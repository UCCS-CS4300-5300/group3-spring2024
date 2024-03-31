from django.db.models import indexes
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.template import loader
from django.views import generic
import json
from . import serializers
from .models import *
from django.templatetags.static import static
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from opensky_api import OpenSkyApi

'''
General Views
'''
class FlightList(generic.ListView):
    model = Flight

class FlightDetail(generic.DetailView):

    model = Flight
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)   

        flight_instance = FlightList()
        flight_list = flight_instance.get_queryset()

        context['flight_list'] = flight_list

        return context
    
#home view
def home(request):
  response = serializers.FlightListView.get(request)
  binary = response.content
  data = json.loads((binary).decode())
  return render(request, 'flightcomparison/home.html', {'flights': data['data']})

# flight search blank, before entering anything into search
def flight_search(request):
    static_url = static('data/airport-codes.csv')
    response = serializers.FlightListView.get(request)
    binary = response.content
    data = json.loads((binary).decode())
    return render(request, 'flightcomparison/flight_search_blank.html', {'flights': data['data'], 'static_url': static_url})

# flight search data, once the user enters data into search form
def flight_search_data(request):
    #for comparison, when asking to compare specific flights, redirects to comparison page
    if request.method == 'POST':
        flight1 = request.POST.get('flight1', '')
        flight2 = request.POST.get('flight2', '')
        sort = request.POST.get('sortoption', '')
        flight1 = get_object_or_404(Flight, pk=flight1)
        flight2 = get_object_or_404(Flight, pk=flight2)
        return redirect('compare', flight_1_id=flight1.id, flight_2_id=flight2.id, sort=sort)
    #loads all data based on user input from search (normal search data)
    static_url = static('data/airport-codes.csv')
    departure_location = request.GET.get('departure_location', '')
    arrival_location = request.GET.get('arrival_location', '')
    departure_time = request.GET.get('departure_time', '')
    price = request.GET.get('price', '')

    flights = Flight.objects.all()
    if departure_location:
        flights = flights.filter(departure_location__icontains=departure_location[7:])
    if arrival_location:
        flights = flights.filter(arrival_location__icontains=arrival_location[7:])
    if departure_time:
        flights = flights.filter(departure_time=departure_time)
    if price:
        flights = flights.filter(price=price)
    
    return render(request, 'flightcomparison/flight_search_data.html', {'flights': flights, 'static_url': static_url})

# runs comparison for specific flights
def compare(request, flight_1_id, flight_2_id, sort):
    flight1 = get_object_or_404(Flight, pk=flight_1_id)
    flight2 = get_object_or_404(Flight, pk=flight_2_id)

    return render(request, 'flightcomparison/flight_compare.html', {'flight1': flight1, 'flight2': flight2, 'sort': sort})


# reference https://openskynetwork.github.io/opensky-api/python.html#

@csrf_exempt
def get_arrivals_by_airport(request, airport, begin, end):
    api = OpenSkyApi()
    arrivals = api.get_arrivals_by_airport(airport, begin, end)
    arrivals_json = [arr.__dict__ for arr in arrivals]
    return JsonResponse(arrivals_json, safe=False)

@csrf_exempt
def get_departures_by_airport(request, airport, begin, end):
    api = OpenSkyApi()
    departures = api.get_departures_by_airport(airport, begin, end)
    departures_json = [dep.__dict__ for dep in departures]
    return JsonResponse(departures_json, safe=False)

@csrf_exempt
def get_flights_by_aircraft(request, icao24, begin, end):
    api = OpenSkyApi()
    flights = api.get_flights_by_aircraft(icao24, begin, end)
    flights_json = [flight.__dict__ for flight in flights]
    return JsonResponse(flights_json, safe=False)

@csrf_exempt
def get_flights_from_interval(request, begin, end):
    api = OpenSkyApi()
    flights = api.get_flights_from_interval(begin, end)
    flights_json = [flight.__dict__ for flight in flights]
    return JsonResponse(flights_json, safe=False)

@csrf_exempt
def get_my_states(request, time_secs=0, icao24=None, serials=None):
    api = OpenSkyApi()
    my_states = api.get_my_states(time_secs, icao24, serials)
    my_states_json = my_states.__dict__
    return JsonResponse(my_states_json, safe=False)

@csrf_exempt
def get_states(request, time_secs=0, icao24=None, bbox=()):
    api = OpenSkyApi()
    states = api.get_states(time_secs, icao24, bbox)
    states_json = states.__dict__
    return JsonResponse(states_json, safe=False)

@csrf_exempt
def get_track_by_aircraft(request, icao24, t=0):
    api = OpenSkyApi()
    track = api.get_track_by_aircraft(icao24, t)
    track_json = track.__dict__
    return JsonResponse(track_json, safe=False)
