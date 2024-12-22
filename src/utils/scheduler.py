from apscheduler.schedulers.background import BackgroundScheduler
from utils.config import TIME_DELAY
from core.fetch_videos import pullYoutubeVideos


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=pullYoutubeVideos,
                      trigger="interval", seconds=TIME_DELAY)
    scheduler.start()
