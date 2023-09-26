import os
from datetime import timedelta
import openpyxl
from django.http import HttpResponse
from django.utils import timezone
from rest_framework.views import APIView
from robots.models import Robot


class GenerateExcelReportView(APIView):
    def get(self, request):
        start_date, end_date = self.get_date_range()
        robot_models = self.get_distinct_robot_models()
        workbook = self.generate_report(robot_models, start_date, end_date)
        return self.create_response(workbook, start_date)

    def get_date_range(self):
        end_date = timezone.now()
        start_date = end_date - timedelta(days=7)
        return start_date, end_date

    def get_distinct_robot_models(self):
        return Robot.objects.values("model").distinct()

    def generate_report(self, robot_models, start_date, end_date):
        workbook = openpyxl.Workbook()
        for model in robot_models:
            model_name = model["model"]
            model_data = self.get_model_data(model_name, start_date, end_date)
            if model_data.exists():
                worksheet = workbook.create_sheet(title=model_name)
                worksheet.append(["Модель", "Версия", "Количество за неделю"])
                version_counts = self.calculate_version_counts(model_data)
                for version, count in version_counts.items():
                    worksheet.append([model_name, version, count])
        return workbook

    def get_model_data(self, model_name, start_date, end_date):
        return Robot.objects.filter(
            model=model_name, created__range=(start_date, end_date)
        )

    def calculate_version_counts(self, model_data):
        version_counts = {}
        for data in model_data:
            version = data.version
            if version in version_counts:
                version_counts[version] += 1
            else:
                version_counts[version] = 1
        return version_counts

    def create_response(self, workbook, start_date):
        temp_file_path = f"excel_report_{start_date.strftime('%Y-%m-%d')}.xlsx"
        workbook.save(temp_file_path)
        response = HttpResponse(content_type="application/octet-stream")
        response[
            "Content-Disposition"
        ] = f'attachment; filename="{temp_file_path}"'
        response["Content-Length"] = os.path.getsize(temp_file_path)
        with open(temp_file_path, "rb") as excel_file:
            response.write(excel_file.read())
        return response
