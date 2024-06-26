import urllib

import requests
from django.http import FileResponse, JsonResponse
from rest_framework import generics, status
from moviepy.editor import AudioFileClip
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.response import Response

from .models import Audio
from .serializers import AudioSerializer


class AudioListCreateAPIView(generics.ListCreateAPIView):
    queryset = Audio.objects.all()
    serializer_class = AudioSerializer


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


@receiver(post_save, sender=Audio)
def convert_and_send_audio_on_save(sender, instance, created, **kwargs):
    if created:
        convert_and_send_audio(instance)


from django.http import JsonResponse


class AudioRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Audio.objects.all()
    serializer_class = AudioSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # Получение URL файла
        file = instance.file.url

        # Получение заголовка
        title = instance.title

        # Возвращаем данные в виде JSON-ответа
        return JsonResponse({'title': title, 'file': file})


class AudioRetrieveWithSubtitlesAPIView(generics.RetrieveAPIView):
    queryset = Audio.objects.all()
    serializer_class = AudioSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        language = request.query_params.get('language', 'kg')
        subtitles = instance.subtitles
        if language in ['ru', 'en']:
            subtitles = self.translate_to_language(subtitles, language)

        response_data = {
            'id': instance.id,
            'title': instance.title,
            'subtitles': subtitles,
        }

        return Response(response_data, status=status.HTTP_200_OK)

    def translate_to_language(self, text, target_language):
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=ky&tl={target_language}&dt=t&q=" + urllib.parse.quote(
            text)
        response = requests.get(url)
        if response.status_code == 200:
            translated_text = response.json()[0][0][0]
            return translated_text
        else:
            return text
