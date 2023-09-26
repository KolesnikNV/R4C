from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Robot


@receiver(pre_save, sender=Robot)
def calculate_serial(sender, instance, **kwargs):
    if not instance.serial:
        instance.serial = f"{instance.model}-{instance.version}"
