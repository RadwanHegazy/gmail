from rest_framework.test import APITestCase
from django.urls import reverse
from mail.models import MAIL_STATUS
from rest_framework import status
from globals.test_objects import create_headers, create_user, create_mail
from uuid import uuid4

class RetriveMailTestCases(APITestCase):

    def get_mail_by_id(self, id) : 
        return reverse('get_email', args=[id])

    def setUp(self):
        # Create test users
        self.user = create_user(
            username = 't1',
            email = 'sender@test.com',
            full_name = "Sender"
        )
        
        self.mail = create_mail(
            to = self.user,
            status = MAIL_STATUS.okay.value,
        )

        self.mail2 = create_mail()

    def test_get_unauthorized(self) :
        req = self.client.get(
            self.get_mail_by_id(uuid4())
        )
        self.assertEqual(req.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_not_found(self) : 
        req = self.client.get(
            self.get_mail_by_id(self.mail2.id),
            headers=create_headers(self.user)
        )
        self.assertEqual(req.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_success(self) : 
        req = self.client.get(
            self.get_mail_by_id(self.mail.id),
            headers=create_headers(self.user)
        )

        self.assertEqual(req.status_code, status.HTTP_200_OK)
        self.assertEqual(req.json()['get_body'], self.mail.get_body)   
