from rest_framework import serializers


class AudioFileSerializer(serializers.Serializer):
    audio = serializers.FileField()
