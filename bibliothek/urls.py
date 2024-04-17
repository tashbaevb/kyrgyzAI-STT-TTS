from django.urls import path
from . import views as v

urlpatterns = [
    path("all/", v.BookListAPIView.as_view(), name='book-list'),
    path("<int:pk>/", v.BookDetailAPIView.as_view(), name="book-detail"),
]
