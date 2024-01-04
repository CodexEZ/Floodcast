from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.createUser),
    path('login/',views.login),
    path('getbounds/',views.getBounds),
    path('getInfo/',views.getInfo)
]