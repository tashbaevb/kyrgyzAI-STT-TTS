from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='movies/')
    audio_file = models.FileField(upload_to='movies/audio/', null=True, blank=True)
    image = models.ImageField(upload_to='img/')
    subtitles = models.TextField(blank=True, null=True)
