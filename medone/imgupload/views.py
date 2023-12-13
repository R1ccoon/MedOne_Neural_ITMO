from django.http import JsonResponse
from .serializers import AttendanceSerializer
from rest_framework.views import APIView


class image_upload_view(APIView):
    """Process images uploaded by users"""
    def post(self, request):
        title = request.data['title']
        serializer_class = AttendanceSerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()

            data = {
                "columns": {"name": "название анализа", "result": "Численный результат",
                            "norm": "численная норма анализа"},
                "rows": [
                    {"is_composite_analysis": True, "name": "Анализ крови"},
                    {"is_composite_analysis": False, "name": "Анализ на эритроциты", "value": "116", "norm": "",
                     "measurement_unit": "г/л"},
                    {"is_composite_analysis": False, "name": "Анализ на эритроциты", "value": "116", "norm": "130-160",
                     "measurement_unit": "г/л"},
                    {"is_composite_analysis": False, "name": "Анализ на эритроциты", "value": "116", "norm": "130-160",
                     "measurement_unit": "г/л"},
                    {"is_composite_analysis": False, "name": "Анализ на эритроциты", "value": "116", "norm": "130-160",
                     "measurement_unit": "г/л"},
                    {"is_composite_analysis": False, "name": "Анализ на эритроциты", "value": "116", "norm": "130-160",
                     "measurement_unit": "г/л"},
                    {"is_composite_analysis": False, "name": "Анализ на эритроциты", "value": "116", "norm": "130-160",
                     "measurement_unit": "г/л"},
                    {"is_composite_analysis": False, "name": "Анализ на эритроциты", "value": "116", "norm": "130-160",
                     "measurement_unit": "г/л"},
                ]
            }
            return JsonResponse(data)
        else:
            print(serializer_class.errors)
            data = {
                'error': 'xz'
            }
            return JsonResponse(data)
