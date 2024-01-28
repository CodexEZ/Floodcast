import json
import string

import os

import pandas as pd

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

    path = os.path.join(os.getcwd()+ "/static/station.csv")
    df = pd.read_csv(path)
    X = df.drop(["Name","Station Code"],axis=1)
    Y = df.drop(["Lat","Lon"],axis=1)
    knn = KNeighborsClassifier()
    knn.fit(X, Y)
    serializer = CreateUserSerializer(data=request.data)

    if serializer.is_valid():
        try:
            latitude = float(serializer.validated_data["latitude"])
            longitude = float(serializer.validated_data["longitude"])
            res = knn.predict([[latitude,longitude]])
            location = res[0,0]
            station = res[0,1]
            serializer.validated_data["nearestStation"] = location
            serializer.validated_data["stationCode"] = station
            user = serializer.save()
            user.save()
            return Response(serializer.data)
        except:
            return Response({"Enable GPS on your app"})
    else:
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def getNearestStation(request):
    path = os.path.join(os.getcwd()+ "/static/station.csv")
    df = pd.read_csv(path)
    X = df.drop(["Name","Station Code"],axis=1)
    Y = df.drop(["Lat","Lon"],axis=1)
    knn = KNeighborsClassifier()
    knn.fit(X, Y)
    serializer = getNearestStationSerializer(data = request.data)
    if serializer.is_valid():
        latitude = float(serializer.validated_data["latitude"])
        longitude = float(serializer.validated_data["longitude"])
        res = knn.predict([[latitude,longitude]])
        location = res[0,0]
        station = res[0,1]
        return Response({
            "location":location,
            "station":station
            })
    else:
        return Response({serializer.errors})

        


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
def getInfo(request):
    serializer = getInfoSerializer(data = request.data)
    print(request.data)
    if(serializer.is_valid()):
        try:
            instance = Users.objects.get(pk = serializer.data["username"])
            stationCode = instance.stationCode
            data = getData(stationCode)
            return Response(data)
        except:
            return Response({"Some error occurred"})
    else:
        return Response(serializer.errors)
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

import requests

def getData(stationCode : string):
    headers = {
        "Class-Name": "ForecastDetailLayerStationDto"
    }
    url = f"https://ffs.india-water.gov.in/iam/api/layer-station/{stationCode}"
    url2 = f"https://ffs.india-water.gov.in/iam/api/new-entry-data/specification/sorted-page?sort-criteria=%7B%22sortOrderDtos%22:%5B%7B%22sortDirection%22:%22DESC%22,%22field%22:%22id.dataTime%22%7D%5D%7D&page-number=0&page-size=2&specification=%7B%22where%22:%7B%22where%22:%7B%22expression%22:%7B%22valueIsRelationField%22:false,%22fieldName%22:%22id.stationCode%22,%22operator%22:%22eq%22,%22value%22:%22{stationCode}%22%7D%7D,%22and%22:%7B%22expression%22:%7B%22valueIsRelationField%22:false,%22fieldName%22:%22id.datatypeCode%22,%22operator%22:%22eq%22,%22value%22:%22HHS%22%7D%7D%7D,%22and%22:%7B%22expression%22:%7B%22valueIsRelationField%22:false,%22fieldName%22:%22dataValue%22,%22operator%22:%22null%22,%22value%22:%22false%22%7D%7D%7D"
    response = requests.get(url, headers=headers)
    response_current = requests.get(url2)
    json_data_curr = response_current.json()
    json_data = response.json()
    data = {
        "hfl" : json_data["floodForecastStaticStationCode"]["highestFlowLevel"],
        "danger_level" : json_data["floodForecastStaticStationCode"]["dangerLevel"],
        "warning_level": json_data["floodForecastStaticStationCode"]["warningLevel"],
        "current_level": json_data_curr[0]['dataValue']
    }
    return data
