from rest_framework import serializers
from .models import Users,Pings
from django.contrib.auth.models import User
from django.utils import timezone

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(allow_null=False)
    password = serializers.CharField(allow_null=False)


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(allow_null=False)


class getInfoSerializer(serializers.Serializer):
    username = serializers.CharField(allow_null=False)

class getNearestStationSerializer(serializers.Serializer):
    latitude = serializers.FloatField(allow_null=False)
    longitude = serializers.FloatField(allow_null=False)

class getLoc(serializers.ModelSerializer):
    class Meta:
        model = Pings
        fields = ["longitude", "latitude"]
