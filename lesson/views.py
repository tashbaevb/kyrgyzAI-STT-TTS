from rest_framework import generics, status
from rest_framework.response import Response
from moviepy.editor import AudioFileClip
from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
from rest_framework.views import APIView

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
        questions_data = []

        # Получить список вопросов, связанных с данным экземпляром Reading
        questions = instance.questions.all()

        # Пройти по каждому вопросу и получить текст и варианты ответов
        for question in questions:
            question_data = {
                "text": question.text,
                "options": [{"id": answer.id, "text": answer.text} for answer in question.answers.all()]
            }
            questions_data.append(question_data)

        return Response(questions_data)


class SpeakingListCreateAPIView(generics.ListCreateAPIView):
    queryset = Speaking.objects.all()
    serializer_class = SpeakingSerializer


def send_audio_to_stt(audio_file):
    headers = {
        'Authorization': 'Bearer e4b038f10b807136fe0c6dfa339a1bd576eca77dfc9cd2ee88a4a289c00e387688ae8b49055300bed5ffb735d18594772784c2e66840bb794c24fdf77ebac3d9'
    }
    response = requests.post('https://asr.ulut.kg/api/receive_data', files={'audio': audio_file}, headers=headers)
    return response


def convert_and_send_audio(instance):
    audio_file_path = instance.file.path

    # Divide files into 25sec videos
    parts = []
    audio = AudioFileClip(audio_file_path)
    duration = audio.duration
    start = 0
    while start < duration:
        end = min(start + 25, duration)
        part = audio.subclip(start, end)
        part_path = audio_file_path.replace('.mp3', f'_part{len(parts) + 1}.mp3')
        part.write_audiofile(part_path)
        parts.append(part_path)
        start = end

    instance.audio_files = parts
    instance.save()

    # Send to another server
    subtitles = ''
    for part_path in parts:
        with open(part_path, 'rb') as audio_file:
            response = send_audio_to_stt(audio_file)

            if response.status_code == 200:
                subtitles += response.json().get('text', '')

    # Save subtitle in Audio
    instance.subtitles = subtitles
    instance.save()


@receiver(post_save, sender=Speaking)
def convert_and_send_audio_on_save(sender, instance, created, **kwargs):
    if created:
        convert_and_send_audio(instance)


class SpeakingRetrieveWithSubtitlesAPIView(generics.RetrieveAPIView):
    queryset = Speaking.objects.all()
    serializer_class = SpeakingSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        subtitles = instance.subtitles

        response_data = {
            'id': instance.id,
            'subtitles': subtitles,
        }

        return Response(response_data, status=status.HTTP_200_OK)
