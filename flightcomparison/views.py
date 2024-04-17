from django.urls import reverse
from django.db.models import indexes
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.template import loader
from django.views import generic
from django.conf import settings
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
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
        print(request.POST.getlist('flights[]'),"flights selected")
        selected_flight_ids = request.POST.getlist('flights[]')
        # flight1 = request.POST.get('flight1', '')
        # flight2 = request.POST.get('flight2', '')
        sort = request.POST.get('sortoption', '')
        # flight1 = get_object_or_404(Flight, pk=flights[0])
        # flight2 = get_object_or_404(Flight, pk=flight2)
        return redirect('compare/list', flight_ids=','.join(selected_flight_ids), sort=sort)
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
def compare(request, flight_ids, sort):
    # list view
    # flight1 = get_object_or_404(Flight, pk=flight_1_id)
    # flight2 = get_object_or_404(Flight, pk=flight_2_id)
    flight_ids = flight_ids
    selected_flights = [int(x) for x in flight_ids.split(',')]
    selected_flights = Flight.objects.filter(id__in=selected_flights)    
    if sort == 'earlydepart':
        selected_flights = selected_flights.order_by('departure_time')
    elif sort == 'latestdepart':
        selected_flights = selected_flights.order_by('-departure_time')
    elif sort == 'earlyarrival':
        selected_flights = selected_flights.order_by('arrival_time')
    elif sort == 'latestarrival':
        selected_flights = selected_flights.order_by('-arrival_time')
    elif sort == 'price':
        selected_flights = selected_flights.order_by('price')  
    # dictionaries for map view
    flights_dict = json.dumps(Flight.get_all_flights_data(), cls=DjangoJSONEncoder)
    return render(request, 'flightcomparison/flight_compare.html', {'flights': selected_flights, 'flight_ids':flight_ids, 'flights_dict':flights_dict, 'sort': sort})

def api_calls(request):
    if request.method == 'GET':
        try:
            return render(request, 'flightcomparison/api_calls.html')
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Invalid request method'})
