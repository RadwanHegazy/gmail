from rest_framework.test import APITestCase
from django.urls import reverse
from mail.models import MAIL_STATUS
from rest_framework import status
from globals.test_objects import create_headers, create_user, create_mail

class SpammedMailsTestCases(APITestCase):
    def setUp(self):
        # Create test users
        self.user = create_user(
            username = 't1',
            email = 'sender@test.com',
            full_name = "Sender"
        )
        
        self.mail = create_mail(
            to = self.user,
            status = MAIL_STATUS.spammed.value,
        )

        self.mail2 = create_mail(
            to = self.user,
            status = MAIL_STATUS.okay.value,
        )

        self.starred_endpoint = reverse('spammed_emails')
    
    def test_unauthorized(self) : 
        req = self.client.get(self.starred_endpoint)
        self.assertEqual(req.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_success(self) : 
        req = self.client.get(self.starred_endpoint, headers=create_headers(self.user))
        self.assertEqual(req.status_code, status.HTTP_200_OK)
        self.assertEqual(req.json()['count'], 1)
    
    def test_get_empty(self) : 
        self.mail.status = MAIL_STATUS.okay.value
        self.mail.save()
        req = self.client.get(self.starred_endpoint, headers=create_headers(self.mail.reciver))
        self.assertEqual(req.status_code, status.HTTP_200_OK)
        self.assertEqual(req.json()['count'], 0)