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
  flight_instance = FlightList()
  flight_list = flight_instance.get_queryset()
  return render(request, 'flightcomparison/home.html', {'flight_list': flight_list})


def flight_search(request):
    if request.method == 'GET':
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

        return render(request, 'flightcomparison/flight_search.html', {'flights': flights})
    else:
        return render(request, 'flightcomparison/flight_search.html')

