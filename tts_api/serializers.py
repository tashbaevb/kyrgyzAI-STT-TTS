from rest_framework import serializers


class TTSSerializer(serializers.Serializer):
    text = serializers.CharField()
    speaker_id = serializers.IntegerField(default=1)
