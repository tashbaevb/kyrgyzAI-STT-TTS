from django.urls import path
from . import views

urlpatterns = [
    path('grammar/', views.GrammarListCreateAPIView.as_view(), name='grammar-list-create'),
    path('grammar/<int:pk>/', views.GrammarRetrieveAPIView.as_view(), name='grammar-detail'),

    path('listening/<int:pk>/audio/', views.get_audio, name='get_audio'),
    path('listening/<int:pk>/submit_answer/', views.submit_answer, name='submit_answer'),

    path('reading/<int:pk>/test/', views.ReadingTestAPIView.as_view(), name='reading_test'),
    path('reading/<int:pk>/', views.ReadingQuestionsAPIView.as_view(), name='reading-questions'),

    path('speaking/', views.SpeakingCreateAPIView.as_view(), name='speaking-create'),
    path('speaking/<int:pk>/compare_audio/', views.SpeakingFileComparisonAPIView.as_view(),
         name='speaking-compare-audio'),

]
