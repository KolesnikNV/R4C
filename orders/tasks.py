from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from utils.models_utils import filter_model
from robots.models import Robot


@shared_task
def send_notification_email(email, robot_serial):
    robot_available = filter_model(Robot, serial=robot_serial)
    model, version = robot_serial.split("-")
    if robot_available:
        subject = "Робот доступен"
        message = f"Добрый день!\nНедавно вы интересовались нашим роботом модели {model} версии {version}. \nЭтот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами."
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]
        send_mail(
            subject, message, from_email, recipient_list, fail_silently=False
        )
