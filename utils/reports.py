import openpyxl
from datetime import datetime, timedelta
from robots.models import Robot


def generate_excel_report():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    robots_data = Robot.objects.filter(created__range=[start_date, end_date])

    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = "Отчет по производству"
    worksheet.append(["Модель", "Версия", "Количество за неделю"])

    for robot in robots_data:
        worksheet.append([robot.model, robot.version, 1])

    return workbook
