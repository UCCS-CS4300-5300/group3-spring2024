from django.contrib import admin
from django.urls import path

from . import views

appName = 'flightcomparison'
urlpatterns = [
    path('', views.home, name='home'),
]