from django.urls import path

from .views import image_upload_view




urlpatterns = [
    path("", image_upload_view.as_view()),
]
