from django.urls import path
from . import views

urlpatterns = [
    path('grammar/', views.GrammarListCreateAPIView.as_view(), name='grammar-list-create'),
    path('grammar/<int:pk>/', views.GrammarRetrieveAPIView.as_view(), name='grammar-detail'),

    path('listening/', views.ListeningListCreateAPIView.as_view(), name='listening-list-create'),
    path('listening/<int:pk>/', views.ListeningDetailAPIView.as_view(), name='listening-detail'),
]
