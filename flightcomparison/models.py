from django.db import models
from django.contrib.auth.models import User
# Create your models here.

'''
Model that Represents an individual flight
'''
class Flight(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    departure_location = models.CharField(max_length=200)
    arrival_location = models.CharField(max_length=200)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    price = models.PositiveIntegerField()
    seat_number = models.PositiveIntegerField()

    def __str__(self):
        return self.user.username + ": " + self.departure_location + " to " + self.arrival_location

    def get_absolute_url(self):
        return reverse('flight_detail', args=[str(self.id)])
    
class FlightData(models.Model):
    icao = models.CharField(max_length=4)
    first_seen = models.IntegerField()
    departure_airport = models.CharField(max_length=4)
    last_seen = models.IntegerField()
    arrival_airport = models.CharField(max_length=4)
    callsign = models.CharField(max_length=8)
    departure_airport_horizontal_distance = models.IntegerField()
    departure_airport_vertical_distance = models.IntegerField()
    arrival_airport_horizontal_distance = models.IntegerField()
    arrival_airport_vertical_distance = models.IntegerField()
    departure_airport_candidates_count = models.IntegerField()
    arrival_airport_candidates_count = models.IntegerField()
