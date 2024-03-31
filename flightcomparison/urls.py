from django.contrib import admin
from django.urls import path

from . import views

appName = 'flightcomparison'
urlpatterns = [
    path('', views.home, name='home'),
    path('flight_search/', views.flight_search, name='flight_search'),
    path('flight_search/query', views.flight_search_data, name='flight_search_data'),
    path('compare/list/<int:flight_1_id>/<int:flight_2_id>/<str:sort>', views.compare, name="compare/list"),
    path('compare/map/<int:flight_1_id>/<int:flight_2_id>/<str:sort>', views.compare, name="compare/map"),
    path('flights/', views.FlightList.as_view(), name='flights'),
    path('flight/<int:pk>/', views.FlightDetail.as_view(), name='flight_detail'),
]