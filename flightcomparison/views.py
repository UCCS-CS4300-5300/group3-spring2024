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
import requests


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


def api_calls(request):
    if request.method == 'GET':
        try:
            return render(request, 'flightcomparison/api_calls.html')
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Invalid request method'})

def get_flights_by_aircraft(request):
    if request.method == 'GET':
        try:
            icao24 = request.GET.get('icao24')
            begin = int(request.GET.get('begin'))
            end = int(request.GET.get('end'))
            url = f"https://opensky-network.org/api/flights/aircraft?icao24={icao24}&begin={begin}&end={end}"
            response = requests.get(url)
            data = response.json()
            flights = data.get('flights', [])
            return JsonResponse({'flights': flights})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Invalid request method'})

def get_arrivals_by_airport(request):
    if request.method == 'GET':
        try:
            airport = request.GET.get('airport')
            begin = int(request.GET.get('begin'))
            end = int(request.GET.get('end'))
            url = f"https://opensky-network.org/api/flights/arrival?airport={airport}&begin={begin}&end={end}"
            response = requests.get(url)
            data = response.json()
            arrivals = data.get('arrivals', [])
            return JsonResponse({'arrivals': arrivals})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Invalid request method'})

def get_departures_by_airport(request):
    if request.method == 'GET':
        try:
            airport = request.GET.get('airport')
            begin = int(request.GET.get('begin'))
            end = int(request.GET.get('end'))
            url = f"https://opensky-network.org/api/flights/departure?airport={airport}&begin={begin}&end={end}"
            response = requests.get(url)
            data = response.json()
            departures = data.get('departures', [])
            return JsonResponse({'departures': departures})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Invalid request method'})

def get_flights_from_interval(request):
    if request.method == 'GET':
        try:
            begin = int(request.GET.get('begin'))
            end = int(request.GET.get('end'))
            url = f"https://opensky-network.org/api/flights/all?begin={begin}&end={end}"
            response = requests.get(url)
            data = response.json()
            flights = data.get('flights', [])
            return JsonResponse({'flights': flights})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Invalid request method'})

def get_my_states(request):
    if request.method == 'GET':
        try:
            time_secs = int(request.GET.get('time_secs', 0))
            icao24 = request.GET.get('icao24')
            serials = request.GET.get('serials')
            url = f"https://opensky-network.org/api/states/own?time={time_secs}&icao24={icao24}&serials={serials}"
            response = requests.get(url)
            data = response.json()
            states = data.get('states', [])
            return JsonResponse({'states': states})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Invalid request method'})

def get_states(request):
    if request.method == 'GET':
        try:
            time_secs = int(request.GET.get('time_secs', 0))
            icao24 = request.GET.get('icao24')
            bbox = request.GET.get('bbox')
            url = f"https://opensky-network.org/api/states/all?time={time_secs}&icao24={icao24}&bbox={bbox}"
            response = requests.get(url)
            data = response.json()
            states = data.get('states', [])
            return JsonResponse({'states': states})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Invalid request method'})

def get_track_by_aircraft(request):
    if request.method == 'GET':
        try:
            icao24 = request.GET.get('icao24')
            t = int(request.GET.get('t', 0))
            url = f"https://opensky-network.org/api/tracks?icao24={icao24}&time={t}"
            response = requests.get(url)
            data = response.json()
            track = data.get('track', [])
            return JsonResponse({'track': track})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Invalid request method'})
