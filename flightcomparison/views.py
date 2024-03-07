from django.db.models import indexes
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.template import loader
from django.views import generic
import json
from . import serializers
from .models import *

'''
General Views
'''
#home view
def home(request):
  response = serializers.FlightListView.get(request)
  binary = response.content
  data = json.loads((binary).decode())
  return render(request, 'home.html', {'flights': data['data']})

def flight_search(request):
    response = serializers.FlightListView.get(request)
    binary = response.content
    data = json.loads((binary).decode())
    return render(request, 'flight_search_blank.html', {'flights': data['data']})

def flight_search_data(request): 
    departure_location = request.GET.get('departure_location', '')
    departure_time = request.GET.get('departure_time', '')
    price = request.GET.get('price', '')

    flights = Flight.objects.all()
    if departure_location:
        flights = flights.filter(departure_location__icontains=departure_location)
    if departure_time:
        flights = flights.filter(departure_time=departure_time)
    if price:
        flights = flights.filter(price=price)

    return render(request, 'flight_search_data.html', {'flights': flights})


'''
Compare views (for flight comparisons)
'''
#have no flights to compare to
def compare(request):
    return render(request, 'compare/compare_blank.html')
#Have one flight to compare to
