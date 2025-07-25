from celery import Celery

from src.config import settings

celery_instance = Celery(
    "tasks",
    backend=settings.REDIS_URL,
    broker=settings.REDIS_URL,
    include=["src.tasks.tasks"],
)

# celery_instance.conf.beat_schedule = {
#     "anything": {
#         "task": "booking_today_checkin",
#         "schedule": 5,
#     }
# }
