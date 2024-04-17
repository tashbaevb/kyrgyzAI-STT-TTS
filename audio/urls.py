from django.urls import path
from . import views

urlpatterns = [
    path('', views.AudioListCreateAPIView.as_view(), name='movie-list-create'),
    path('<int:pk>/', views.AudioRetrieveAPIView.as_view(), name='movie-detail'),
    path('<int:pk>/subtitles/', views.AudioRetrieveWithSubtitlesAPIView.as_view(), name='movie-subtitles'),
]
