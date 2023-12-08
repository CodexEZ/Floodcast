from django.db import models
import numpy as np
# Create your models here.

class Users(models.Model):
    username = models.CharField(max_length=50,primary_key=True,null=False)
    password = models.CharField(max_length=50,null=False)
    name = models.CharField(max_length=100,null=False)
    email = models.EmailField(null=False,default="")
    phone = models.IntegerField(null=False,unique=True,default=0)
    warnings = models.BooleanField(default=False,null=False)
    latitude = models.DecimalField(max_digits=9, decimal_places=6,default=0.00)
    longitude = models.DecimalField(max_digits=9, decimal_places=6,default=0.00)


class Area(models.Model):
    boundary =  models.BinaryField()
    station = models.CharField(max_length=20,primary_key=True,null=False)

    def saveArray(self,array,name):
        self.boundary = array.tobytes()
        self.station = name
        self.save()
    def loadArray(self):
        return np.frombuffer(self.boundary,dtype=np.float32)

