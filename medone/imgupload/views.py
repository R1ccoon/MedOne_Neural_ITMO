import sqlite3

from django.http import JsonResponse
from .serializers import AttendanceSerializer
from rest_framework.views import APIView
from .gemini import start_recognition
from PIL import Image


class image_upload_view(APIView):
    """Process images uploaded by users"""

    def post(self, request):
        title = request.data['title']
        serializer_class = AttendanceSerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            connection = sqlite3.connect('./db.sqlite3')
            cursor = connection.cursor()
            cursor.execute(f'SELECT image FROM imgupload_image WHERE title = "{str(title)}"')
            img = cursor.fetchall()
            f = Image.open(f"./media/{img[0][0]}")
            data = start_recognition(f)
            return JsonResponse(data, safe=False)
        else:
            data = {
                'error': serializer_class.errors
            }
            return JsonResponse(data)
