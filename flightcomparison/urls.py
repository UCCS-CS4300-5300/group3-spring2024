from django.contrib import admin
from django.urls import path

from . import views

appName = 'flightcomparison'
urlpatterns = [
    path('', views.home, name='home'),
    path('flight_search/', views.flight_search, name='flight_search'),
    path('flights/', views.FlightList.as_view(), name='flights'),
    path('flight/<int:pk>/', views.FlightDetail.as_view(), name='flight_detail'),
]