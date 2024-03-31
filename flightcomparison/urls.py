from django.contrib import admin
from django.urls import path

from . import views

appName = 'flightcomparison'
urlpatterns = [
    path('', views.home, name='home'),
    path('flight_search/', views.flight_search, name='flight_search'),
    path('flight_search/query', views.flight_search_data, name='flight_search_data'),
    path('compare/<int:flight_1_id>/<int:flight_2_id>/<str:sort>', views.compare, name="compare"),
    path('flights/', views.FlightList.as_view(), name='flights'),
    path('flight/<int:pk>/', views.FlightDetail.as_view(), name='flight_detail'),
    
    # # Added URL patterns for API methods
    # path('api-calls/', TemplateView.as_view(template_name='api_calls.html'), name='api_calls'),
    # path('get-arrivals-by-airport/', views.get_arrivals_by_airport, name='get_arrivals_by_airport'),
    # path('get-departures-by-airport/', views.get_departures_by_airport, name='get_departures_by_airport'),
    # path('get-flights-by-aircraft/', views.get_flights_by_aircraft, name='get_flights_by_aircraft'),
    # path('get-flights-from-interval/', views.get_flights_from_interval, name='get_flights_from_interval'),
    # path('get-my-states/', views.get_my_states, name='get_my_states'),
    # path('get-states/', views.get_states, name='get_states'),
    # path('get-track-by-aircraft/', views.get_track_by_aircraft, name='get_track_by_aircraft'),
]