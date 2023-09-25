from django.urls import path
from robots.views import CreateRobotView

urlpatterns = [
    path("robots/", CreateRobotView.as_view(), name="robots"),
]
