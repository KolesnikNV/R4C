import os
from celery import Celery
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "R4C.settings")

app = Celery("R4C")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.broker_url = "pyamqp://guest@localhost//"
app.conf.result_backend = "rpc://"

app.conf.beat_schedule = {
    "check-and-send-notifications": {
        "task": "orders.send_notification_email",
        "schedule": timezone.timedelta(hours=12),
    },
}

app.autodiscover_tasks()
