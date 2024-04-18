from django.urls import path
from . import views

urlpatterns = [
    path('grammar/', views.GrammarListCreateAPIView.as_view(), name='grammar-list-create'),
    path('grammar/<int:pk>/', views.GrammarRetrieveAPIView.as_view(), name='grammar-detail'),

    path('listening/', views.ListeningListCreateAPIView.as_view(), name='listening-list-create'),
    path('listening/<int:pk>/', views.ListeningDetailAPIView.as_view(), name='listening-detail'),

    path('reading/<int:pk>/test/', views.ReadingTestAPIView.as_view(), name='reading_test'),
    path('reading/<int:pk>/', views.ReadingQuestionsAPIView.as_view(), name='reading-questions'),

    path('speaking/', views.SpeakingListCreateAPIView.as_view(), name='movie-list-create'),
    path('speaking/<int:pk>/subtitles/', views.SpeakingRetrieveWithSubtitlesAPIView.as_view(), name='movie-subtitles'),
]
