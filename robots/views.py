from rest_framework import generics

from api.serializers import RobotSerializer

from .models import Robot


class CreateRobotView(generics.ListCreateAPIView):
    queryset = Robot.objects.all()
    serializer_class = RobotSerializer
