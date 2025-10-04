from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from listings.models import Listing, Booking

class ListingAPITest(APITestCase):
    def setUp(self):
        self.listing = Listing.objects.create(title="Beach House", description="Nice view", price=150.00)
        self.list_url = reverse('listing-list')
        self.detail_url = reverse('listing-detail', args=[self.listing.id])

    def test_list_listings(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_listing(self):
        data = {"title": "New Villa", "description": "Modern and cozy", "price": 300.00}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_listing(self):
        data = {"title": "Updated House", "description": "Renovated", "price": 200.00}
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated House")

    def test_delete_listing(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class BookingAPITest(APITestCase):
    def setUp(self):
        self.listing = Listing.objects.create(title="Cabin", description="In the woods", price=100.00)
        self.booking = Booking.objects.create(
            listing=self.listing,
            guest_name="John Doe",
            check_in="2025-10-10",
            check_out="2025-10-15",
        )
        self.booking_url = reverse('booking-list')
        self.booking_detail_url = reverse('booking-detail', args=[self.booking.id])

    def test_list_bookings(self):
        response = self.client.get(self.booking_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_booking(self):
        data = {
            "listing": self.listing.id,
            "guest_name": "Jane Smith",
            "check_in": "2025-11-01",
            "check_out": "2025-11-05"
        }
        response = self.client.post(self.booking_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_booking(self):
        data = {
            "listing": self.listing.id,
            "guest_name": "John Updated",
            "check_in": "2025-10-12",
            "check_out": "2025-10-18"
        }
        response = self.client.put(self.booking_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["guest_name"], "John Updated")

    def test_delete_booking(self):
        response = self.client.delete(self.booking_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
