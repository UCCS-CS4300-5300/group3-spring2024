from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Flight, FlightData

import unittest
import requests
from unittest.mock import patch, MagicMock
from base64 import b64encode


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

def fetch_states():
    try:
        response = requests.get("https://opensky-network.org/api/states/all")
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        print('Error:', e)
        raise

def get_own_states():
    username = 'USERNAME'
    password = 'PASSWORD'
    credentials = b64encode(f"{username}:{password}".encode()).decode()
    headers = {'Authorization': f'Basic {credentials}'}

    try:
        response = requests.get("https://opensky-network.org/api/states/own", headers=headers)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        print('Error:', e)
        raise

def get_departures_by_airport(airport, begin, end):
    username = 'USERNAME'
    password = 'PASSWORD'
    credentials = b64encode(f"{username}:{password}".encode()).decode()
    headers = {'Authorization': f'Basic {credentials}'}
    params = {'airport': airport, 'begin': begin, 'end': end}

    try:
        response = requests.get("https://opensky-network.org/api/flights/departure", params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        print('Error:', e)
        raise

def get_arrivals_by_airport(airport, begin, end):
    username = 'USERNAME'
    password = 'PASSWORD'
    credentials = b64encode(f"{username}:{password}".encode()).decode()
    headers = {'Authorization': f'Basic {credentials}'}
    params = {'airport': airport, 'begin': begin, 'end': end}

    try:
        response = requests.get("https://opensky-network.org/api/flights/arrival", params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        print('Error:', e)
        raise

def get_flights_in_time_interval(begin, end):
    username = 'USERNAME'
    password = 'PASSWORD'
    credentials = b64encode(f"{username}:{password}".encode()).decode()
    headers = {'Authorization': f'Basic {credentials}'}
    params = {'begin': begin, 'end': end}

    try:
        response = requests.get("https://opensky-network.org/api/flights/all", params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        print('Error:', e)
        raise

class TestOpenSkyAPI(unittest.TestCase):
    @patch('requests.get')
    def test_fetch_states(self, mock_get):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {'some': 'data'}
        mock_get.return_value = mock_response

        result = fetch_states()

        self.assertEqual(result, {'some': 'data'})
        mock_get.assert_called_once_with(
            "https://opensky-network.org/api/states/all"
        )

    @patch('requests.get')
    def test_get_own_states(self, mock_get):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {'some': 'data'}
        mock_get.return_value = mock_response

        result = get_own_states()

        self.assertEqual(result, {'some': 'data'})
        mock_get.assert_called_once_with(
            "https://opensky-network.org/api/states/own",
            headers={'Authorization': 'Basic VVNFUk5BTUU6UEFTU1dPUkQ='}
        )

    @patch('requests.get')
    def test_get_departures_by_airport(self, mock_get):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {'some': 'data'}
        mock_get.return_value = mock_response

        result = get_departures_by_airport('airport', 'begin', 'end')

        self.assertEqual(result, {'some': 'data'})
        mock_get.assert_called_once_with(
            "https://opensky-network.org/api/flights/departure",
            params={'airport': 'airport', 'begin': 'begin', 'end': 'end'},
            headers={'Authorization': 'Basic VVNFUk5BTUU6UEFTU1dPUkQ='}
        )

    @patch('requests.get')
    def test_get_arrivals_by_airport(self, mock_get):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {'some': 'data'}
        mock_get.return_value = mock_response

        result = get_arrivals_by_airport('airport', 'begin', 'end')

        self.assertEqual(result, {'some': 'data'})
        mock_get.assert_called_once_with(
            "https://opensky-network.org/api/flights/arrival",
            params={'airport': 'airport', 'begin': 'begin', 'end': 'end'},
            headers={'Authorization': 'Basic VVNFUk5BTUU6UEFTU1dPUkQ='}
        )

    @patch('requests.get')
    def test_get_flights_in_time_interval(self, mock_get):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {'some': 'data'}
        mock_get.return_value = mock_response

        result = get_flights_in_time_interval('begin', 'end')

        self.assertEqual(result, {'some': 'data'})
        mock_get.assert_called_once_with(
            "https://opensky-network.org/api/flights/all",
            params={'begin': 'begin', 'end': 'end'},
            headers={'Authorization': 'Basic VVNFUk5BTUU6UEFTU1dPUkQ='}
        )

class CompareViewTestCase(TestCase):
    def setUp(self):
        # Create some Flight objects for testing
        self.user = User.objects.create_user(username='test_user', email='test@example.com', password='password')
        self.flight1 = Flight.objects.create(user=self.user, departure_location='Location 1', departure_location_latitude=40.7128, departure_location_longitude=-74.0060, layover_location='Location 1', layover_location_latitude=40.7128, layover_location_longitude=-74.0060, arrival_location='Location 2', arrival_location_latitude=34.0522, arrival_location_longitude=-118.2437, departure_time='2024-04-25 10:00:00', arrival_time='2024-04-25 12:00:00', price=100, seat_number=50)
        self.flight2 = Flight.objects.create(user=self.user, departure_location='Location 3', departure_location_latitude=37.7749, departure_location_longitude=-122.4194, layover_location='Location 3', layover_location_latitude=37.7749, layover_location_longitude=-122.4194, arrival_location='Location 4', arrival_location_latitude=34.0522, arrival_location_longitude=-118.2437, departure_time='2024-04-25 11:00:00', arrival_time='2024-04-25 13:00:00', price=150, seat_number=60)

    def test_compare_view_latest_depart_sort(self):
        url = reverse('compare/list', args=('1,2', 'latestdepart'))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'flightcomparison/flight_compare.html')
        # Check if flights are sorted by departure time descending
        self.assertQuerysetEqual(response.context['flights'], [self.flight2, self.flight1])

    def test_compare_view_early_arrival_sort(self):
        url = reverse('compare/list', args=('1,2', 'earlyarrival'))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'flightcomparison/flight_compare.html')
        # Check if flights are sorted by arrival time ascending
        self.assertQuerysetEqual(response.context['flights'], [self.flight1, self.flight2])

    def test_compare_view_latest_arrival_sort(self):
        url = reverse('compare/list', args=('1,2', 'latestarrival'))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'flightcomparison/flight_compare.html')
        # Check if flights are sorted by arrival time descending
        self.assertQuerysetEqual(response.context['flights'], [self.flight2, self.flight1])

    def test_compare_view_price_sort(self):
        url = reverse('compare/list', args=('1,2', 'price'))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'flightcomparison/flight_compare.html')
        # Check if flights are sorted by price ascending
        self.assertQuerysetEqual(response.context['flights'], [self.flight1, self.flight2])



