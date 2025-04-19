from rest_framework.test import APITestCase
from globals.test_objects import User, create_user
from django.urls import reverse

class TestRegsiterEndpoint (APITestCase) : 

    def setUp(self) -> None:
        self.register_endpoint = reverse('register')
        
    def test_POST_no_body(self) : 
        req = self.client.post(self.register_endpoint)
        self.assertEqual(req.status_code, 400)
        
    def test_POST_valid_body(self) : 
        req = self.client.post(self.register_endpoint, data={
            'username' : "test",
            'email' : 'test@gmail.com',
            'password' : 'test123',
            'phonenumber' : "+201009670000",
            'picture' : open('globals/test_materials/test.png','rb')
        })
        self.assertEqual(req.status_code, 201)
        self.assertTrue(User.objects.filter(email='test@gmail.com'))
        
    def test_POST_invaild_phonenumber(self) : 
        req = self.client.post(self.register_endpoint, data={
            'username' : "test",
            'email' : 'test@gmail.com',
            'password' : 'test123',
            'phonenumber' : "invalid_phone_number",
            'picture' : open('globals/test_materials/test.png','rb')
        })
        self.assertEqual(req.status_code, 400)
        self.assertFalse(User.objects.filter(email='test@gmail.com').exists())

    def test_POST_exists_email(self):
        # Create initial user with email
        first_user = create_user(email="test@gmail.com")
        
        # Try to create another user with same email
        second_user = self.client.post(self.register_endpoint, data={
            'username': "test2",
            'email': 'test@gmail.com',
            'password': 'test456',
            'phonenumber': "+201009670001",
            'picture': open('globals/test_materials/test.png','rb')
        })
        
        self.assertEqual(second_user.status_code, 400)
        self.assertEqual(User.objects.filter(email='test@gmail.com').count(), 1)
