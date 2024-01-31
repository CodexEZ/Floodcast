from django.db import models
import numpy as np
from django.utils import timezone
# Create your models here.

class Users(models.Model):
    username = models.CharField(max_length=50,primary_key=True,null=False)
    password = models.CharField(max_length=50,null=False)
    email = models.EmailField(default="",null=False)
    latitude = models.DecimalField(max_digits=9, decimal_places=6,default=0.00,null=False)
    longitude = models.DecimalField(max_digits=9, decimal_places=6,default=0.00,null=False)
    nearestStation = models.CharField(null = False,max_length=50,default="")
    stationCode = models.CharField(null=False,max_length=50,default="")

class Area(models.Model):
    boundary =  models.BinaryField()
    station = models.CharField(max_length=20,primary_key=True,null=False)

    def saveArray(self,array,name):
        self.boundary = array.tobytes()
        self.station = name
        self.save()
    def loadArray(self):
        return np.frombuffer(self.boundary,dtype=np.float32)

class Pings(models.Model):
    id = models.CharField(auto_created=True, primary_key=True,max_length=5)
    latitude = models.FloatField(null=False)
    longitude = models.FloatField(null=False)
    timestamp = models.DateTimeField(default=timezone.now)