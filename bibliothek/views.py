from rest_framework import generics

from . import models as m, serializers as s


class BookListAPIView(generics.ListAPIView):
    queryset = m.Book.objects.all()
    serializer_class = s.BookSerializer


class BookDetailAPIView(generics.RetrieveAPIView):
    queryset = m.Book.objects.all()
    serializer_class = s.BookSerializer
