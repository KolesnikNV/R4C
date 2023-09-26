import re

from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class RobotValidator:
    def __call__(self, data):
        model = data.get("model")
        version = data.get("version")
        created = data.get("created")

        if (
            not isinstance(model, str)
            or not isinstance(version, str)
            or len(model) != 2
            or len(version) != 2
            or isinstance(created, str)
        ):
            raise serializers.ValidationError(
                "Model и Version должны быть строками из 2 символов"
            )


class OrderValidator:
    def __call__(self, data):
        email = data.get("email")
        robot_serial = data.get("robot_serial")

        if not isinstance(email, str) or not isinstance(robot_serial, str):
            raise serializers.ValidationError(
                "Email и Robot_serial должны быть строками."
            )
        if (
            not re.match(r"^[A-Za-z0-9]*-[A-Za-z0-9]*$", robot_serial)
            or len(robot_serial) != 5
        ):
            raise ValidationError(
                "Серийный номер должен состоять из 5 символов и содержать буквы, цифры и символ '-'."
            )
