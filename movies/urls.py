from django.urls import path
from . import views

urlpatterns = [
    path('', views.MovieListCreateAPIView.as_view(), name='movie-list-create'),
    path('<int:pk>/', views.MovieRetrieveAPIView.as_view(), name='movie-detail'),
    path('<int:pk>/subtitles/', views.MovieRetrieveWithSubtitlesAPIView.as_view(), name='movie-subtitles'),
]
