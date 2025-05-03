from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from globals.test_objects import create_headers, create_user
from uuid import uuid4

class SpamUsersTestCases(APITestCase):

    def setUp(self):
        # Create test users
        self.user = create_user(
            username = 't1',
            email = 'Rec@test.com',
            full_name = "Reciver"
        )

        self.user2 = create_user(
            username = 't2',
            email = 'tst13@gmailc.om',
            full_name = "Reciver2"
        )
        self.headers = create_headers(self.user)

        self.spam_endpoint = reverse('create_spam')

    def test_unauthorized(self) : 
        req = self.client.post(
            self.spam_endpoint
        )
        self.assertEqual(req.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_spam_not_found_user(self) : 
        req = self.client.post(
            self.spam_endpoint,
            headers=self.headers,
            data={
                'spam_user_id' : str(uuid4())
            }
        )
        self.assertEqual(req.status_code, status.HTTP_400_BAD_REQUEST)


    def test_spam_myself(self) : 
        req = self.client.post(
            self.spam_endpoint,
            headers=self.headers,
            data={
                'spam_user_id' : str(self.user.id)
            }
        )
        self.assertEqual(req.status_code, status.HTTP_400_BAD_REQUEST)

    def test_spam_success(self) :
        req = self.client.post(
            self.spam_endpoint,
            headers=self.headers,
            data={
                'spam_user_id' : str(self.user2.id)
            }
        )
        self.assertEqual(req.status_code, status.HTTP_201_CREATED)