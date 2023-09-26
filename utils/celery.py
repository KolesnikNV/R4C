from __future__ import absolute_import, unicode_literals
import os
from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "R4C.settings")

app = Celery("R4C")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.broker_url = "pyamqp://guest@localhost//"
app.conf.result_backend = "rpc://"

app.autodiscover_tasks()
