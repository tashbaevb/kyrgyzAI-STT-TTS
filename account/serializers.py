from rest_framework import serializers
from . import models as m


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = m.User
        fields = ['username', 'email', 'password']


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = m.User
        fields = ['email', 'password']