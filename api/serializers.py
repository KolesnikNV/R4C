from rest_framework import serializers

from orders.models import Order
from robots.models import Robot

from .validators import OrderValidator, RobotValidator


class RobotSerializer(serializers.ModelSerializer):
    serial = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Robot
        fields = ("model", "version", "created", "serial")

    def get_serial(self, obj):
        return f"{obj.model}-{obj.version}"

    def validate(self, data):
        validator = RobotValidator()
        validator(data)
        return data


class OrderSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    robot_serial = serializers.CharField()

    class Meta:
        model = Order
        fields = ("email", "robot_serial")

    def validate(self, data):
        validator = OrderValidator()
        validator(data)
        return data
