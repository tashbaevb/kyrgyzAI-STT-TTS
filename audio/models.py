from django.db import models


class Audio(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='audios/')
    audio_file = models.FileField(upload_to='audios/audio/', null=True, blank=True)
    subtitles = models.TextField(blank=True, null=True)
