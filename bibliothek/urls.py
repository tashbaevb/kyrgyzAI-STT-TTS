from django.urls import path
from . import views as v

urlpatterns = [
    path("", v.BookListCreateAPIView.as_view(), name='book-list-create'),
    path("all/", v.BookListAPIView.as_view(), name='book-list'),
    path("<int:pk>/translate/", v.BookDetailAPIView.as_view(), name="book-detail"),
]
