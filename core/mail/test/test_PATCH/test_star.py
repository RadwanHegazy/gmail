from rest_framework.test import APITestCase
from django.urls import reverse
from mail.models import MAIL_STATUS, Mail
from rest_framework import status
from globals.test_objects import create_headers, create_user, create_mail
from uuid import uuid4

class StarMailTestCases(APITestCase):
    def setUp(self):
        # Create test users
        self.user = create_user(
            username = 't1',
            email = 'sender@test.com',
            full_name = "Sender"
        )
        self.headers = create_headers(self.user)
        
        self.mail = create_mail(
            to = self.user,
            status = MAIL_STATUS.okay.value
        )

    def read_endpoint(self, id) : 
        return reverse('star_mail', args=[id])

    def test_unaithorized(self) : 
        req = self.client.patch(
            self.read_endpoint(uuid4())
        )
        self.assertEqual(req.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_found_email(self) : 
        req = self.client.patch(
            self.read_endpoint(uuid4()),
            headers=self.headers
        )
        self.assertEqual(req.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_success(self) : 
        req = self.client.patch(
            self.read_endpoint(self.mail.id),
            headers=self.headers
        )
        self.assertEqual(req.status_code, status.HTTP_200_OK)
        response = req.json()
        mail = Mail.objects.get(
            id=response['id']
        )
        self.assertEqual(mail.status, MAIL_STATUS.starred.value)