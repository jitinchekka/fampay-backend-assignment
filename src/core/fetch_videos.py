from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from utils import config
from models import Video, FetchHistory
from datetime import datetime
from database import get_db
import redis
import logging
from sqlalchemy.dialects.sqlite import insert

ISO_DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

redis_working = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    redis_client = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)
    redis_client.ping()
    redis_working = True
except:
    print("Unable to connect to redis")


def get_currenttime():
    return datetime.now().strftime(ISO_DATE_FORMAT)


def get_last_fetch_info():
    with next(get_db()) as db:
        return db.query(FetchHistory).order_by(FetchHistory.last_fetch_time.desc()).first()


def update_fetch_history(db, last_video_id, last_fetch_time):
    fetch_history = FetchHistory(
        last_video_id=last_video_id,
        last_fetch_time=datetime.strptime(last_fetch_time, ISO_DATE_FORMAT),
    )
    db.add(fetch_history)


def process_youtube_response(response, db):
    videos_to_insert = []
    last_video_id = None

    for search_result in response.get("items", []):
        video = Video(
            video_id=search_result["id"]["videoId"],
            title=search_result["snippet"]["title"],
            description=search_result["snippet"]["description"],
            published_at=datetime.strptime(
                search_result["snippet"]["publishedAt"], ISO_DATE_FORMAT
            ),
            thumbnails=str(search_result["snippet"]
                           ["thumbnails"]["high"]["url"]),
        )
        videos_to_insert.append(video.__dict__)
        last_video_id = video.video_id

    for video_dict in videos_to_insert:
        video_dict.pop('_sa_instance_state', None)

    if videos_to_insert:
        stmt = insert(Video).values(videos_to_insert)
        stmt = stmt.on_conflict_do_nothing(index_elements=['video_id'])

        result = db.execute(stmt)
        logger.info(f"Processed {len(videos_to_insert)} videos, inserted {
                    result.rowcount} new videos.")

    return last_video_id


def fetch_videos_from_youtube(published_after_date):
    keys_to_skip = {}
    key_index = 0

    while True:
        key = config.GOOGLE_API_KEYS[key_index]
        if key in keys_to_skip:
            key_index = (key_index + 1) % len(config.GOOGLE_API_KEYS)
            continue

        try:
            youtube = build(
                YOUTUBE_API_SERVICE_NAME,
                YOUTUBE_API_VERSION,
                developerKey=key,
            )
            search_response = (
                youtube.search()
                .list(
                    q=config.QUERY,
                    type="video",
                    part="snippet",
                    maxResults=50,
                    order="date",
                    publishedAfter=published_after_date.strftime(
                        ISO_DATE_FORMAT),
                )
                .execute()
            )

            # Handle all database operations in a single transaction
            with next(get_db()) as db:
                try:
                    last_video_id = process_youtube_response(
                        search_response, db)
                    current_time = get_currenttime()
                    update_fetch_history(db, last_video_id, current_time)

                    # Commit everything in one transaction
                    db.commit()
                    logger.info(
                        f"Successfully committed videos and fetch history.")

                    # Update Redis after successful commit
                    if redis_working:
                        redis_client.set("last_successful_fetch", current_time)

                except Exception as e:
                    db.rollback()
                    logger.error(f"Database transaction failed: {
                                 str(e)}", exc_info=True)
                    raise

            logger.info(f"Successful fetch from YouTube API: {key}")
            break

        except HttpError as e:
            logger.error(f"Failed to fetch videos from YouTube API: {key}")
            if "quotaExceeded" in str(e):
                keys_to_skip[key] = True
                if len(keys_to_skip) == len(config.GOOGLE_API_KEYS):
                    logger.error("All keys have exceeded quota.")
                    return
            else:
                logger.error(f"Error details: {str(e)}")
                continue

        key_index = (key_index + 1) % len(config.GOOGLE_API_KEYS)


def pullYoutubeVideos():
    '''
    This function fetches videos from YouTube APIs.
    '''
    logger.info("Starting pullYoutubeVideos job")
    try:
        last_successful_fetch = None
        if redis_working:
            last_successful_fetch = redis_client.get("last_successful_fetch")
        last_fetch_info = get_last_fetch_info()
        published_after_date = (
            datetime.strptime(last_successful_fetch.decode(), ISO_DATE_FORMAT)
            if last_successful_fetch
            else last_fetch_info.last_fetch_time
            if last_fetch_info
            else datetime(2025, 1, 12)
        )

        fetch_videos_from_youtube(published_after_date)
        logger.info("Completed pullYoutubeVideos job")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)