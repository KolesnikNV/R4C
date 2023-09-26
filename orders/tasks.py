from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from robots.models import Robot
from django.utils import timezone


@shared_task
def send_notification_email(email, robot_serial):
    if robots_available := Robot.objects.filter(
        available_date__gte=timezone.now() - timezone.timedelta(hours=12),
        serial=robot_serial,
    ):
        subject = "Робот доступен"
        model, version = robot_serial.split("-")
        message = f"Добрый день!\nНедавно вы интересовались нашим роботом модели {model} версии {version}. \nЭтот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами."
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = email
        send_mail(
            subject, message, from_email, recipient_list, fail_silently=False
        )
