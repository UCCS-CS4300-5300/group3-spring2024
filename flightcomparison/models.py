from django.db import models
from django.contrib.auth.models import User

from opensky_api import OpenSkyApi
# Create your models here.

'''
Model that Represents an individual flight
'''
class Flight(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    departure_location = models.CharField(max_length=200)
    departure_location_latitude = models.DecimalField(max_digits=200,decimal_places=10)
    departure_location_longitude = models.DecimalField(max_digits=200,decimal_places=10)
    layover_location = models.CharField(max_length=200)
    layover_location_latitude = models.DecimalField(max_digits=200,decimal_places=10)
    layover_location_longitude = models.DecimalField(max_digits=200,decimal_places=10)
    arrival_location = models.CharField(max_length=200)
    arrival_location_latitude = models.DecimalField(max_digits=200,decimal_places=10)
    arrival_location_longitude = models.DecimalField(max_digits=200,decimal_places=10)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    price = models.PositiveIntegerField()
    seat_number = models.PositiveIntegerField()

    def __str__(self):
        return self.user.username + ": " + self.departure_location + " to " + self.arrival_location

    def get_absolute_url(self):
        return reverse('flight_detail', args=[str(self.id)])
    
'''
Model represents all data from the OpenSky Network API
'''
class FlightData(models.Model):
    #24bit hex transponder value
    icao24 = models.CharField(max_length=200)
    #estimated departure time
    firstSeen = models.IntegerField()
    #estimated departure airport (ICAO code)
    estDepartureAirport = models.CharField(max_length=10)
    #estimated arrival time
    lastSeen = models.IntegerField()
    #estimated arrival airport (ICAO code)
    estArrivalAirport = models.CharField(max_length=10)
    #Call sign of the plane
    callsign = models.CharField(max_length=8)

    #positional data
    #horizontal and vertical distances of last recieved airborne position to departure airport in meters
    estDepartureAirportHorizDistance = models.IntegerField()
    estDepartureAirportVertDistance = models.IntegerField()
    #Horizontal and vertical distances of last recieved airborne positions to arrival airport in meters
    estArrivalAirportHorizDistance = models.IntegerField()
    estArrivalAirportVertDistance = models.IntegerField()

    #number of other possible departure and arrival points
    departureAirportCandidatesCount = models.IntegerField()
    arrivalAirportCandidatesCount = models.IntegerField()

    def __str__(self):
        return self.icao24 + ": " + self.estDepartureAirport + " " + self.estArrivalAirport
    
    def get_tracking_data(self):
        api = OpenSkyApi()
        return api.get_track_by_aircraft(self.icao24)
