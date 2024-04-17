from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField(upload_to='movies/')
    audio_file = models.FileField(upload_to='movies/audio/', null=True, blank=True)
    subtitles = models.TextField(blank=True, null=True)
