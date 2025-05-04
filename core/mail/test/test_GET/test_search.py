from rest_framework.test import APITestCase
from django.urls import reverse
from mail.models import MAIL_STATUS
from rest_framework import status
from globals.test_objects import create_headers, create_user, create_mail

class SearchMailsTestCases(APITestCase):

    def search_endpoint(self, keyword) : 
        return reverse('search_emails') + "?q=" + keyword

    def setUp(self):
        # Create test users
        self.user = create_user(
            username = 't1',
            email = 'Rec@test.com',
            full_name = "Reciver"
        )
        self.headers = create_headers(self.user)
        
        self.mail = create_mail(
            to = self.user,
            status = MAIL_STATUS.okay.value,
            header="Happy Eid !",
        )

        self.mail2 = create_mail(
            to = self.user,
            status = MAIL_STATUS.okay.value,
            header="Eid Saeed",
        )

        self.mail3 = create_mail(
            to = self.user,
            status = MAIL_STATUS.okay.value,
            header="Email Confirm",
        )


    def test_unauthorized(self) : 
        req = self.client.get(
            self.search_endpoint('test')
        )
        self.assertEqual(req.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_search_no_results(self) : 
        req = self.client.get(
            self.search_endpoint('test'),
            headers=self.headers
        )
        self.assertEqual(req.status_code, status.HTTP_200_OK)
        self.assertEqual(req.json()['count'], 0)


    def test_search_results(self) : 
        req = self.client.get(
            self.search_endpoint('Eid'),
            headers=self.headers
        )
        self.assertEqual(req.status_code, status.HTTP_200_OK)
        self.assertNotEqual(req.json()['count'], 2)
    
 
