from rest_framework import serializers
from robots.models import Robot
from .robot_validators import RobotValidator


class RobotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Robot
        fields = ("model", "version", "created")
        extra_kwargs = {
            "serial": {"read_only": True},
        }

    def create_serial_field(self, data):
        model = data.get("model")
        version = data.get("version")
        return f"{model}-{version}"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.context.get("request").method == "GET":
            data["serial"] = self.create_serial_field(data)
        return data

    def validate(self, data):
        validator = RobotValidator()
        validator(data)
        return data
