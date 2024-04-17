import requests
from django.http import FileResponse
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


class AudioRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Audio.objects.all()
    serializer_class = AudioSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        file_path = instance.file.path
        file_response = FileResponse(open(file_path, 'rb'))

        serializer = self.get_serializer(instance)
        movie_data = serializer.data

        # Add a data_fields to response
        file_response.data = movie_data

        return file_response


class AudioRetrieveWithSubtitlesAPIView(generics.RetrieveAPIView):
    queryset = Audio.objects.all()
    serializer_class = AudioSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
