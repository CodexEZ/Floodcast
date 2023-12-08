import json

from django.shortcuts import render
from rest_framework.response import  Response
from .Serializers import *
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Users



@api_view(['POST'])
def createUser(request):
    serializer = CreateUserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if(serializer.is_valid()):
        try:
            instance = Users.objects.get(pk = serializer.data['username'])
        except:
            return Response({"User doesn't exist"},status=status.HTTP_404_NOT_FOUND)
        if(instance.password == serializer.data['password']):
            return Response(serializer.data)
        else:
            return Response({"Wrong password"},status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def forgot_password_username(request):
    serializer = ForgotPasswordSerializer(data=request.data)
    results = Users.objects.filter(email = serializer.data['email'])
    if results.exists():
        #Add email recovery functionality here
        return Response({"Mail has been sent to your mail"})

@api_view(['GET'])
def getBounds(request):
    f = open("D:/SIH2023/Backend/backend/api/bounds.geojson","r")
    geojson_data = json.load(f)
    return Response(geojson_data)

