from rest_framework.test import APITestCase
from globals.test_objects import User, create_user, create_headers
from django.urls import reverse

class TestProfileEndpoint (APITestCase) : 

    def setUp(self) -> None:
        self.profile_endpoint = reverse('profile')
        self.user = create_user()
        self.headers = create_headers(self.user)

    def test_GET_unauthorized_user(self):
        # Test GET request without authorization
        response = self.client.get(self.profile_endpoint)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_GET_success(self):
        # Test successful GET request with valid authorization
        response = self.client.get(
            self.profile_endpoint,
            headers=self.headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['username'], self.user.username)
        