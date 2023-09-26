from django.urls import path

from orders.views import CreateOrder
from robots.views import CreateRobotView
from utils.reports import GenerateExcelReportView

urlpatterns = [
    path("robots/", CreateRobotView.as_view(), name="robots"),
    path("download/", GenerateExcelReportView.as_view(), name="exel"),
    path("create_order/", CreateOrder.as_view(), name="create-order"),
]
