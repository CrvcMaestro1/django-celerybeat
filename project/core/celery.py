import os

from celery import Celery
from celery.schedules import crontab
import core.tasks

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "sample_task": {
        "task": "core.tasks.sample_task",
        "schedule": crontab(minute="*/1"),
    },
    "send_email_report": {
        "task": "core.tasks.send_email_report",
        "schedule": crontab(hour="*/1"),
    }
}
