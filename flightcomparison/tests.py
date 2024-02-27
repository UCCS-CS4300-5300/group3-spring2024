from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Flight

class FlightModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_flight_creation(self):
        # Tests the creation of a Flight instance and verifies attributes.
        flight = Flight.objects.create(
            user=self.user,
            departure_location="City A",
            arrival_location="City B",
            departure_time=timezone.now(),
            arrival_time=timezone.now(),
            price=100,
            seat_number=1
        )
        self.assertEqual(flight.departure_location, "City A")
        self.assertEqual(flight.arrival_location, "City B")
        # Tests the __str__ method returns expected string format.
        self.assertEqual(flight.__str__(), 'testuser: City A to City B')

class HomeViewTests(TestCase):
    def test_home_view_status_code(self):
        # Tests that the home view returns a 200 status code.
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_home_view_uses_correct_template(self):
        # Tests that the home view uses the correct template.
        url = reverse('home')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'home.html')

class FlightSearchViewTests(TestCase):
    def setUp(self):
        # Creates a Flight instance for testing the search functionality.
        self.user = User.objects.create_user(username='testuser', password='12345')
        Flight.objects.create(
            user=self.user,
            departure_location="City A",
            arrival_location="City B",
            departure_time=timezone.now(),
            arrival_time=timezone.now(),
            price=100,
            seat_number=1
        )

    def test_search_by_departure_location(self):
        # Tests flight search functionality filters by departure location.
        response = self.client.get(reverse('flight_search'), {'departure_location': 'City A'})
        self.assertContains(response, "City A")
        self.assertNotContains(response, "No flights found.")
        
