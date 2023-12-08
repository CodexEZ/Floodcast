from rest_framework import serializers
from .models import Users
from django.contrib.auth.models import User

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(allow_null=False)
    password = serializers.CharField(allow_null=False)

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(allow_null=False)