from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from models import Post

ARCHIVE_RETENTION_DAYS: int = 7


def cleanup_archived_threads():
    cutoff_date = datetime.now() - timedelta(days=ARCHIVE_RETENTION_DAYS)
    query = Post.delete().where(Post.is_archived == True, Post.bumped_at < cutoff_date)
    deleted_count = query.execute()
    print(f"Deleted {deleted_count} archived threads older than {ARCHIVE_RETENTION_DAYS} days")


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(cleanup_archived_threads, 'interval', days=7)
    scheduler.start()
