from django.urls import path
from robots.views import CreateRobotView
from utils.reports import GenerateExcelReportView

urlpatterns = [
    path("robots/", CreateRobotView.as_view(), name="robots"),
    path("download/", GenerateExcelReportView.as_view(), name="exel"),
]
