from django.db import models
from django.contrib.auth.models import User
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