from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from . import views

appName = 'flightcomparison' 
urlpatterns = [
    path('', views.flight_search, name='flight_search'), 
    path('recommendations/', views.recommend, name='recommend'), 
    path('flight_search/query/', views.flight_search_data, name='flight_search_data'), 
    path('compare/list/<str:flight_ids>/<str:sort>', views.compare, name="compare/list"),
    path('compare/map/<str:flight_ids>/<str:sort>/', views.compare, name="compare/map"), 
    path('flights/', views.FlightList.as_view(), name='flights'), 
    path('flight/<int:pk>/', views.FlightDetail.as_view(), name='flight_detail'), 
    path('api-calls/', views.api_calls, name='api_calls'),
]
