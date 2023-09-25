from datetime import datetime
from rest_framework import serializers


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
