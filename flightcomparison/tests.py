from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Flight, FlightData

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
            departure_location_latitude = 1,
            departure_location_longitude = 1,
            layover_location = "City C",
            layover_location_latitude = 1,
            layover_location_longitude = 1,
            arrival_location_latitude = 1,
            arrival_location_longitude = 1,
            arrival_time=timezone.now(),
            price=100,
            seat_number=1
        )
        self.assertEqual(flight.departure_location, "City A")
        self.assertEqual(flight.arrival_location, "City B")
        # Tests the __str__ method returns expected string format.
        self.assertEqual(flight.__str__(), 'testuser: City A to City B')

    def test_FlightData_creation(self):
        flight = FlightData.objects.create(
            icao24 = "CODE",
            firstSeen = 1234,
            estDepartureAirport = "KDEN",
            lastSeen = 1,
            estArrivalAirport = "KGRB",
            callsign = "SIGN",

            estDepartureAirportHorizDistance = 1,
            estDepartureAirportVertDistance = 1,
            estArrivalAirportHorizDistance = 1,
            estArrivalAirportVertDistance = 1,
            departureAirportCandidatesCount = 1,
            arrivalAirportCandidatesCount = 1
        )

        #asserting the important data is correct
        self.assertEqual(flight.estDepartureAirport, "KDEN")
        self.assertEqual(flight.estArrivalAirport, "KGRB")
        self.assertEqual(flight.firstSeen, 1234)

        #testing functions related to model
        self.assertEqual(flight.__str__(), "CODE: KDEN KGRB")

class UserInterfaceTests(TestCase):
    '''
    Home View
    '''
    def test_recommend_view_status_code(self):
        # Tests that the home view returns a 200 status code.
        url = reverse('recommend')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_recommend_view_uses_correct_template(self):
        # Tests that the home view uses the correct template.
        url = reverse('recommend')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'flightcomparison/recommend.html')

    '''
    Flight_Search view
    '''
    def test_flight_search_status_code(self):
        #tests that the flight_search page returns a 200 status code
        url = reverse('flight_search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_flight_search_correct_template(self):
        #tests that the blank template was used
        url = reverse('flight_search')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'flightcomparison/flight_search_blank.html')

    def test_flight_search_post_status_code(self):
        #tests that the post code works
        url = reverse('flight_search')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)

    '''
    Flight_Compare View
    '''
    def test_flight_compare_get_status_code(self):
        #tests that the flight compare status code is correct
        #creates flight to compare against
        self.user = User.objects.create_user(username='testuser', password='12345')
        Flight.objects.create(
            user=self.user,
            departure_location="City A",
            arrival_location="City B",
            departure_location_latitude = 1,
            departure_location_longitude = 1,
            layover_location = "City C",
            layover_location_latitude = 1,
            layover_location_longitude = 1,
            arrival_location_latitude = 1,
            arrival_location_longitude = 1,
            departure_time=timezone.now(),
            arrival_time=timezone.now(),
            price=100, 
            seat_number=1
        )
        url = reverse('compare/list', kwargs={'flight_1_id': 1, 'flight_2_id': 1, 'sort': 'price'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_flight_compare_correct_template(self):
        #creates flight to compare against
        self.user = User.objects.create_user(username='testuser', password='12345')
        Flight.objects.create(
            user=self.user,
            departure_location="City A",
            arrival_location="City B",
            departure_location_latitude = 1,
            departure_location_longitude = 1,
            layover_location = "City C",
            layover_location_latitude = 1,
            layover_location_longitude = 1,
            arrival_location_latitude = 1,
            arrival_location_longitude = 1,
            departure_time=timezone.now(),
            arrival_time=timezone.now(),
            price=100,
            seat_number=1
        )
        #tests to make sure the flight_compare template is being used
        url = reverse('compare/list', kwargs={'flight_1_id': 1, 'flight_2_id': 1, 'sort': 'price'})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'flightcomparison/flight_compare.html')
    

class FlightSearchTests(TestCase):
    def setUp(self):
        # Creates a Flight instance for testing the search functionality.
        self.user = User.objects.create_user(username='testuser', password='12345')
        Flight.objects.create(
            user=self.user,
            departure_location="City A",
            arrival_location="City B",
            departure_location_latitude = 1,
            departure_location_longitude = 1,
            layover_location = "City C",
            layover_location_latitude = 1,
            layover_location_longitude = 1,
            arrival_location_latitude = 1,
            arrival_location_longitude = 1,
            departure_time=timezone.now(),
            arrival_time=timezone.now(),
            price=100,
            seat_number=1
        )

    def test_search_by_departure_location(self):
        # Tests flight search functionality filters by departure location.
        response = self.client.get(reverse('flight_search_data'), {'departure_location': 'City A'})
        self.assertContains(response, "City A")
        self.assertNotContains(response, "No flights found.")

