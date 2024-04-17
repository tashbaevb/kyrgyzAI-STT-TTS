from rest_framework import generics
from rest_framework.response import Response
import requests

from .models import Grammar, Listening, Reading, Speaking
from .serializers import GrammarSerializer, ListeningSerializer, ReadingSerializer, SpeakingSerializer


class GrammarListCreateAPIView(generics.ListCreateAPIView):
    queryset = Grammar.objects.all()
    serializer_class = GrammarSerializer


class GrammarRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Grammar.objects.all()
    serializer_class = GrammarSerializer


class ListeningCreateAPIView(generics.CreateAPIView):
    queryset = Listening.objects.all()
    serializer_class = ListeningSerializer


class ListeningListCreateAPIView(generics.ListCreateAPIView):
    queryset = Listening.objects.all()
    serializer_class = ListeningSerializer

    def post(self, request, *args, **kwargs):
        # Получение текста из запроса
        text = request.data.get('text', '')

        # Сохранение текста в базе данных
        listening = Listening.objects.create(text=text)

        # Возвращение ответа с данными текста
        serializer = self.get_serializer(listening)
        return Response(serializer.data)


def text_to_speech(text):
    data = {'text': text, 'speaker_id': 1}

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer e4b038f10b807136fe0c6dfa339a1bd576eca77dfc9cd2ee88a4a289c00e387688ae8b49055300bed5ffb735d18594772784c2e66840bb794c24fdf77ebac3d9'
    }

    response = requests.post('http://tts.ulut.kg/api/tts', json=data, headers=headers)

    return response


class ListeningDetailAPIView(generics.RetrieveAPIView):
    queryset = Listening.objects.all()
    serializer_class = ListeningSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()

        # Отправка текста на другой API для преобразования в mp3 файл
        response = text_to_speech(instance.text)

        # Проверка ответа и возврат результата
        if response.status_code == 200:
            return Response(response.content, content_type=response.headers['Content-Type'])
        else:
            return Response({'error': 'Ошибка при отправке текста на API text_to_speech'}, status=response.status_code)


class ReadingListCreateAPIView(generics.ListCreateAPIView):
    queryset = Reading.objects.all()
    serializer_class = ReadingSerializer


class SpeakingListCreateAPIView(generics.ListCreateAPIView):
    queryset = Speaking.objects.all()
    serializer_class = SpeakingSerializer
