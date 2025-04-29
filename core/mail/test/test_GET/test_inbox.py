from rest_framework.test import APITestCase
from django.urls import reverse
from mail.models import Mail
from rest_framework import status
from globals.test_objects import create_headers, create_user, create_mail

class InboxTestCase(APITestCase):
    def setUp(self):
        # Create test users
        self.sender = create_user(
            username = 't1',
            email = 'sender@test.com',
            full_name = "Sender"
        )
        
        self.reciver = create_user(
            email='reciver@test.com',
            password='testpass123',
            username='t2',
            full_name='Reciver'
        )
        
        # Create test mails
        self.mail1 = create_mail(
            from_=self.sender,
            to=self.reciver,
            header='Test Mail 1',
            body='Test Content 1'.encode(),
            is_read=False,
            status='okay'
        )
        self.mail2 = create_mail(
            from_=self.sender,
            to=self.reciver,
            header='Test Mail 2',
            body='Test Content 2'.encode(),
            is_read=True,
            status='okay'
        )

        self.mail3 = create_mail(
            from_=self.reciver,
            to=self.sender,
            header='Test Mail 3',
            body='Test Content 3'.encode(),
            is_read=False,
            status='okay'
        )
        
        # URL for inbox endpoint
        self.inbox_url = reverse('inbox')
        

    def test_get_inbox_success(self):
        """Test retrieving inbox mails successfully"""
        response = self.client.get(self.inbox_url, headers=create_headers(self.reciver))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['count'], 2)
        
    def test_get_inbox_unauthorized(self):
        """Test unauthorized access to inbox"""
        response = self.client.get(self.inbox_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_inbox_mail_content(self):
        """Test the body of inbox mails"""
        response = self.client.get(self.inbox_url, headers=create_headers(self.reciver))
        data = response.json()['results']
        
        self.assertEqual(data[0]['header'], 'Test Mail 2')
        self.assertEqual(data[0]['sender_full_name'], self.sender.full_name)
        self.assertTrue(data[0]['is_read'])
        
    def test_sender_inbox(self):
        """Test empty inbox"""
        response = self.client.get(self.inbox_url, headers=create_headers(self.sender))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['count'], 1)
        
