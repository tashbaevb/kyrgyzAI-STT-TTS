from django.urls import path
from . import views

urlpatterns = [
    path('', views.speech_to_text, name='speech_to_text'),
]
