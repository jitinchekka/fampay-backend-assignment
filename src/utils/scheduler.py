from threading import Lock
from apscheduler.schedulers.background import BackgroundScheduler
from utils.config import TIME_DELAY
from core.fetch_videos import pullYoutubeVideos

job_lock = Lock()


def locked_pullYoutubeVideos():
    if not job_lock.acquire(blocking=False):
        print("Another instance of the job is already running.")
        return
    try:
        pullYoutubeVideos()
    finally:
        job_lock.release()


def start_scheduler():
    print(f"Times delay is set to {TIME_DELAY} seconds.")
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=locked_pullYoutubeVideos,
                      trigger="interval", seconds=TIME_DELAY)

    scheduler.start()
