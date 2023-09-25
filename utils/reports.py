from rest_framework.views import APIView
from datetime import timedelta
import openpyxl
from robots.models import Robot
import os
from django.http import HttpResponse
from django.utils import timezone


class GenerateExcelReportView(APIView):
    def get(self, request):
        end_date = timezone.now()
        start_date = end_date - timedelta(days=7)
        robot_models = Robot.objects.values("model").distinct()
        workbook = openpyxl.Workbook()

        for model in robot_models:
            model_name = model["model"]
            model_data = Robot.objects.filter(
                model=model_name, created__range=(start_date, end_date)
            )

            if model_data.exists():
                worksheet = workbook.create_sheet(title=model_name)
                worksheet.append(["Модель", "Версия", "Количество за неделю"])

                version_counts = {}
                for data in model_data:
                    version = data.version
                    if version in version_counts:
                        version_counts[version] += 1
                    else:
                        version_counts[version] = 1

                for version, count in version_counts.items():
                    worksheet.append([model_name, version, count])

        temp_file_path = f"excel_report_{start_date.strftime('%Y-%m-%d')}.xlsx"
        workbook.save(temp_file_path)

        response = HttpResponse(content_type="application/octet-stream")
        response["Content-Disposition"] = f'attachment; filename="{temp_file_path}"'
        response["Content-Length"] = os.path.getsize(temp_file_path)

        with open(temp_file_path, "rb") as excel_file:
            response.write(excel_file.read())

        return response
