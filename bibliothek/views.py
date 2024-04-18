import urllib

import requests
from rest_framework import generics, status
from rest_framework.response import Response

from . import models as m, serializers as s
from .models import Book
from .serializers import BookSerializer


class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookListAPIView(generics.ListAPIView):
    queryset = m.Book.objects.all()
    serializer_class = s.BookSerializer


class BookDetailAPIView(generics.RetrieveAPIView):
    queryset = m.Book.objects.all()
    serializer_class = s.BookSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        language = request.query_params.get('language', 'kg')  # Defaults

        content = instance.content
        if language in ['ru', 'en']:  # Translate to another language
            content = self.translate_to_language(content, language)

        response_data = {
            'id': instance.id,
            'title': instance.title,
            'content': content,
        }

        return Response(response_data, status=status.HTTP_200_OK)

    def translate_to_language(self, text, target_language):
        # Перевод текста на целевой язык с помощью Google Translate API
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=ky&tl={target_language}&dt=t&q=" + urllib.parse.quote(
            text)
        response = requests.get(url)
        if response.status_code == 200:
            translated_text = response.json()[0][0][0]
            return translated_text
        else:
            return text
