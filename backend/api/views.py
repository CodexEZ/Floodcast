import json
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import joblib
from django.shortcuts import render
from rest_framework.response import  Response
from .Serializers import *
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Users
from sklearn.neighbors import KNeighborsClassifier




#This view basically accepts user data, along with his location i.e latitude and longitude, fits it into KNN classifier
#to find the nearest water monitoring station and saves it in the data base

#The API format will be ->
# {
#   "username": "",
#   "password": "",
#   "email": "",
#   "latitude": 0,
#   "longitude": 0,
#   "nearestStation": ""
# }
@api_view(['POST'])
def createUser(request):
    df = pd.read_csv("D:/Aswin's project/Backend/backend/api/station.csv")
    df = df.drop("Station Code", axis=1)
    X = df["Name"]
    Y = df.drop("Name", axis=1)
    knn = KNeighborsClassifier(n_neighbors=1)
    knn.fit(Y, X)
    serializer = CreateUserSerializer(data=request.data)
    print(serializer.fields)
    if serializer.is_valid():
        latitude = float(serializer.validated_data["latitude"])
        longitude = float(serializer.validated_data["longitude"])
        location = knn.predict([[latitude,longitude]])
        serializer.validated_data["nearestStation"] = location[0]
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

