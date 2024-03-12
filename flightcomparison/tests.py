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
    '''
    Home View
    '''
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
        self.assertTemplateUsed(response, 'flight_search_blank.html')

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
            departure_time=timezone.now(),
            arrival_time=timezone.now(),
            price=100,
            seat_number=1
        )
        url = reverse('compare', kwargs={'flight_1_id': 1, 'flight_2_id': 1, 'sort': 'price'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_flight_compare_correct_template(self):
        #creates flight to compare against
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
        #tests to make sure the flight_compare template is being used
        url = reverse('compare', kwargs={'flight_1_id': 1, 'flight_2_id': 1, 'sort': 'price'})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'flight_compare.html')
    

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
        
