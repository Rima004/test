from http.client import responses

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.users.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import RefreshToken

# Create your tests here.
class TestUsers(APITestCase):

    def setUp(self):
        self.register_data = {
            "first_name": "user",
            "last_name":"2",
            "email": "user2@gmail.com",
            "password": "user2",
            "username":"user1"
        }

        self.user=User.objects.create_user( first_name="user",last_name="1",email="user1@gmail.com",password="user1",username="user1")
        self.token=RefreshToken.for_user(self.user)
        self.access_token=str(self.token.access_token)




    def test_register(self):
        response=self.client.post(reverse('register'),self.register_data,format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_token(self):
        data={"email":self.user.email,
              "password":"user1"}
        response=self.client.post(reverse("token_obtain_pair"),data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_refresh(self):
        data={
            "refresh":self.token
        }
        response=self.client.post(reverse("token_refresh"),data)

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertIn('access',response.data)

    def test_list_user(self):

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        responses =self.client.get(reverse("list"))

        self.assertEqual(responses.status_code,status.HTTP_200_OK)




