from rest_framework import serializers
from . import models


class GrammarSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Grammar
        fields = '__all__'



class ReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reading
        fields = '__all__'


class SpeakingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Speaking
        fields = '__all__'
