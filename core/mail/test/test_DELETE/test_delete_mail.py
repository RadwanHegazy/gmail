from rest_framework.test import APITestCase
from django.urls import reverse
from mail.models import MAIL_STATUS, Mail
from rest_framework import status
from globals.test_objects import create_headers, create_user, create_mail
from uuid import uuid4

class DeleteMailTestCases(APITestCase):
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

    def delete_endpoint(self, id) : 
        return reverse('delete_mail', args=[id])

    def test_unauthorized(self) : 
        req = self.client.delete(
            self.delete_endpoint(uuid4())
        )
        self.assertEqual(req.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_not_found(self) : 
        req = self.client.delete(
            self.delete_endpoint(uuid4()),
            headers=self.headers
        )
        self.assertEqual(req.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_no_permission(self) : 
        req = self.client.delete(
            self.delete_endpoint(self.mail.id),
            headers=create_headers(create_user())
        )
        self.assertEqual(req.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_delete_success(self) : 
        req = self.client.delete(
            self.delete_endpoint(self.mail.id),
            headers=self.headers
        )
        self.assertEqual(req.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(
            Mail.objects.get(id=self.mail.id).status,
            MAIL_STATUS.deleted.value
        )
        