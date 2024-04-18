import os
import tempfile
import requests
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Listening


from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from moviepy.editor import AudioFileClip
from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
from rest_framework.views import APIView

from .models import Grammar, Reading, Speaking, Listening
from .serializers import GrammarSerializer, SpeakingSerializer


class GrammarListCreateAPIView(generics.ListCreateAPIView):
    queryset = Grammar.objects.all()
    serializer_class = GrammarSerializer


class GrammarRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Grammar.objects.all()
    serializer_class = GrammarSerializer


import tempfile


@api_view(['GET'])
def get_audio(request, pk):
    try:
        listening = Listening.objects.get(pk=pk)
        text_to_convert = listening.answer

        # Отправить текст на API для преобразования в аудио
        data = {'text': text_to_convert, 'speaker_id': 1}
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer e4b038f10b807136fe0c6dfa339a1bd576eca77dfc9cd2ee88a4a289c00e387688ae8b49055300bed5ffb735d18594772784c2e66840bb794c24fdf77ebac3d9'
        }
        response = requests.post('http://tts.ulut.kg/api/tts', json=data, headers=headers)

        if response.status_code != 200:
            return Response({'error': 'Ошибка при отправке данных на другой backend'}, status=response.status_code)

        # Создать временный файл и записать в него аудиоданные
        temp_file_path = os.path.join(tempfile.gettempdir(), f'audio_{pk}.mp3')
        with open(temp_file_path, 'wb') as temp_file:
            temp_file.write(response.content)

        # Сохранить путь к файлу в объекте Listening
        listening.audio_file = temp_file_path
        listening.save()

        # Получить URL файла
        file_url = request.build_absolute_uri(listening.audio_file.url)

        # Вернуть URL в качестве ответа
        return Response({'audio_url': file_url}, status=status.HTTP_200_OK)

    except Listening.DoesNotExist:
        return Response({'error': 'Listening not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def submit_answer(request, pk):
    try:
        listening = Listening.objects.get(pk=pk)
        user_answer = request.data.get('user_answer', '')
        # Получаем правильный ответ из объекта Listening
        correct_answer = listening.answer
        # Сравниваем ответы
        is_correct = user_answer.strip().lower() == correct_answer.strip().lower()
        # Отмечаем тест как завершенный
        listening.is_finished = True
        listening.save()
        # Возвращаем результат сравнения
        return Response({'is_correct': is_correct}, status=status.HTTP_200_OK)
    except Listening.DoesNotExist:
        return Response({'error': 'Listening not found'}, status=status.HTTP_404_NOT_FOUND)


class ReadingTestAPIView(APIView):
    def post(self, request, pk):
        reading = Reading.objects.get(pk=pk)
        answers = request.data.get('answers', {})

        correct_answers, total_questions = reading.check_answers(answers)

        result = {
            'correct_answers': correct_answers,
            'total_questions': total_questions
        }

        return Response(result)


class ReadingQuestionsAPIView(generics.RetrieveAPIView):
    queryset = Reading.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # Получить title и content экземпляра Reading
        title = instance.title
        content = instance.content

        questions_data = {
            "title": title,
            "content": content,
            "questions": []
        }

        # Получить список вопросов, связанных с данным экземпляром Reading
        questions = instance.questions.all()

        # Пройти по каждому вопросу и получить текст и варианты ответов
        for question in questions:
            question_data = {
                "text": question.text,
                "options": [{"id": answer.id, "text": answer.text} for answer in question.answers.all()]
            }
            questions_data["questions"].append(question_data)

        return Response(questions_data)


def send_audio_to_stt(audio_file):
    # Заголовки запроса с токеном авторизации
    headers = {
        'Authorization': 'Bearer e4b038f10b807136fe0c6dfa339a1bd576eca77dfc9cd2ee88a4a289c00e387688ae8b49055300bed5ffb735d18594772784c2e66840bb794c24fdf77ebac3d9'
    }

    # Формирование POST запроса с файлом аудио
    files = {'audio': audio_file}
    response = requests.post('https://asr.ulut.kg/api/receive_data', files=files, headers=headers)

    return response


class SpeakingCreateAPIView(generics.CreateAPIView):
    queryset = Speaking.objects.all()
    serializer_class = SpeakingSerializer


class SpeakingFileComparisonAPIView(generics.GenericAPIView):
    queryset = Speaking.objects.all()
    serializer_class = SpeakingSerializer

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        user_audio_file = request.FILES.get('audio_file')

        # Преобразуйте аудиофайл в текст с помощью вашего метода send_audio_to_stt
        response = send_audio_to_stt(user_audio_file)

        if response.status_code == 200:
            user_text = response.json().get('text', '')
            correct_text = instance.text
            is_correct = user_text.strip().lower() == correct_text.strip().lower()

            return Response({'is_correct': is_correct}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Ошибка при отправке аудиофайла на сервер распознавания речи'},
                            status=response.status_code)
