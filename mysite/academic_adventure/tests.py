import datetime

from django.test import TestCase
from django.test.client import Client
from django.utils import timezone
from django.urls import reverse

from .models import Event

class EventModelTest(TestCase):
    """
    Tests for the event model in the database
    """
    def event_is_recent_with_future_event(self):
        """
        recent() returns False for events that are not within
        2 hours in the future
        """

        time = timezone.now() + datetime.timedelta(hours=3)
        future_event = Event(date=time)

        self.assertIs(future_event.recent(), False)
    
    def event_is_recent_with_recent_event(self):
        """
        recent() returns True for events that are within the next
        2 hours in the future
        """

        time = timezone.now() + datetime.timedelta(hours=1.5)
        current_event = Event(date=time)

        self.assertIs(current_event.recent(), True)
    
    def event_is_recent_with_previous_event(self):
        """
        recent() returns False for events that are in the past
        """

        time = timezone.now() - datetime.timedelta(hours=0.2)
        previous_event = Event(date=time)

        self.assertIs(previous_event.recent(), False)
    
    def event_is_recent_with_boundary_event(self):
        """
        recent() returns True for events exactly 2 hours in the future
        """

        time = timezone.now() + datetime.timedelta(hours=2)
        current_event = Event(date = time)

        self.assertIs(current_event.recent(), True)   
    
    def event_is_joinable(self):
        """
        joinable() should return True if the current time is between 10 minutes before an events start time and 5 minutes after

        Keyword arguments:
        self -- TestCase obejct to allow for the method to be run as a Django test
        """

        time = timezone.now() + datetime.timedelta(minutes=5)
        current_event = Event(date=time)

        self.assertIs(current_event.joinable(), True)
    
    def event_is_joinable_lower_boundary(self):
        """
        joinable() should return True if the current time is between 10 minutes before an events start time and 5 minutes after.
        This tests the lower boundary (10 mins before).

        Keyword arguments:
        self -- TestCase obejct to allow for the method to be run as a Django test
        """

        time = timezone.now() - datetime.timedelta(minutes=10)
        current_event = Event(date=time)

        self.assertIs(current_event.joinable(), True)
    
    def event_is_joinable_upper_boundary(self):
        """
        joinable() should return True if the current time is between 10 minutes before an events start time and 5 minutes after.
        This tests the upper boundary (5 mins after the start).

        Keyword arguments:
        self -- TestCase obejct to allow for the method to be run as a Django test
        """

        time = timezone.now() + datetime.timedelta(minutes=5)
        current_event = Event(date=time)

        self.assertIs(current_event.joinable(), True)
    
    def event_is_joinable_invalid_lower(self):
        """
        joinable() should return false if the event is too far in the past

        Keyword arguments:
        self -- TestCase obejct to allow for the method to be run as a Django test
        """
        time = timezone.now() - datetime.timedelta(minutes=11)
        current_event = Event(date=time)

        self.assertIs(current_event.joinable(), False)
    
    def event_is_joinable_invalid_higher(self):
        """
        joinable() should return false if the event is too far in the future

        Keyword arguments:
        self -- TestCase obejct to allow for the method to be run as a Django test
        """
        time = timezone.now() + datetime.timedelta(minutes=6)
        current_event = Event(date=time)

        self.assertIs(current_event.joinable(), False)
    
    def event_is_joinable_past_day(self):
        """
        joinable() should return false if the event is on another day in the past

        Keyword arguments:
        self -- TestCase obejct to allow for the method to be run as a Django test
        """
        time = timezone.now() - datetime.timedelta(days=1)
        current_event = Event(date=time)

        self.assertIs(current_event.joinable(), False)
    
    def event_is_joinable_future_day(self):
        """
        joinable() should return false if the event is on another day in the future

        Keyword arguments:
        self -- TestCase obejct to allow for the method to be run as a Django test
        """
        time = timezone.now() + datetime.timedelta(days=1)
        current_event = Event(date=time)

        self.assertIs(current_event.joinable(), False)

class LoginTest(TestCase):
    """
    Tests for the login view
    """

    def test_login_GET(self):
        """
        Test the login view when the user is not logged in
        """
        client = Client()
        response = client.get("/academic-adventure/login/")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")

    def test_login_success(self):
        """
        Test the login view when the user is logged in.
        Should redirect the user to the home page.
        """
        client = Client()
        response = client.post("/academic-adventure/login/", follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("home.html")


class HomeViewTest(TestCase):
    """
    Tests for the home view
    """
    
    def test_home_GET(self):
        """
        Tests a GET request for the homepage, should return and render
        home.html
        """
        client = Client()
        response = client.get(reverse("academic_adventure:home"), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("home.html")


class EventsViewTest(TestCase):
    """
    Tests for the map view
    """

    def test_events_GET(self):
        """
        Tests GET method on map view. Should return the map.html page
        """
        client = Client()
        response = client.get(reverse("academic_adventure:events"), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("events.html")


class LeaderboardViewTest(TestCase):
    """
    Tests for the leaderboard view
    """

    def test_leaderboard_GET(self):
        """
        Tests the GET method on the leaderboard view.
        Should return the leaderboard.html page
        """
        client = Client()
        response = client.get(reverse("academic_adventure:leaderboard"), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("leaderboard.html")


class CreateViewTest(TestCase):
    """
    Tests the create view which allows gamekeepers to create events
    """

    def test_create_GET(self):
        """
        Tests the GET method on the create view. Should return the
        create.html page
        """
        client = Client()
        response = client.get(reverse("academic_adventure:create"), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("create.html")

    def test_create_POST(self):
        """
        Tests when the POST method is used on the view. Should redirect the user
        to the code.html page
        """
        client = Client()
        response = client.post(reverse("academic_adventure:create"), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("code.html")


class ScanViewTest(TestCase):
    """
    Tests the scan view which allows a user to scan a QR code to 
    join an event
    """

    def test_scan_GET(self):
        client = Client()
        response = client.get(reverse("academic_adventure:create"), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("scan.html")
