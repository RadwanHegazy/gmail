from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from globals.test_objects import create_headers, create_user, Mail
from uuid import uuid4

class CreateMailTestCase(APITestCase):
    
    def setUp(self):
        self.user = create_user(
            username = 't1',
            email = 'sender@test.com',
            full_name = "Sender"
        )

        self.create_endpoint = reverse('create_email')
        self.headers = create_headers(self.user)

    def test_unauthorized(self) : 
        req = self.client.post(self.create_endpoint)
        self.assertEqual(req.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_no_body(self) : 
        req = self.client.post(self.create_endpoint, headers=self.headers)
        self.assertEqual(req.status_code, status.HTTP_400_BAD_REQUEST)

    def test_success_no_attachments_reciver_not_found(self):
        body = {
            'body' : "<h1>This is my Body!!!</h1>",
            'header' : "Normal Header.",
            'reciver' : str(uuid4())
        }
        req = self.client.post(
            self.create_endpoint,
            headers=self.headers,
            data=body
        )

        self.assertEqual(req.status_code, status.HTTP_400_BAD_REQUEST)

    def test_success_no_attachments_reciver_found(self):
        reciver = create_user()
        body = {
            'body' : "<h1>This is my Body!!!</h1>",
            'header' : "Normal Header.",
            'reciver' : str(reciver.id)
        }
        req = self.client.post(
            self.create_endpoint,
            headers=self.headers,
            data=body
        )

        self.assertEqual(req.status_code, status.HTTP_201_CREATED)


        