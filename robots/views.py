from rest_framework import generics
from .models import Robot
from api.serializers import RobotSerializer


class CreateRobotView(generics.ListCreateAPIView):
    queryset = Robot.objects.all()
    serializer_class = RobotSerializer
