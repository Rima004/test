from http.client import responses

from django.template.base import kwarg_re
from django.test import TestCase
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from apps.tasks.models import Task
from apps.users.models import User
from rest_framework import status
from rest_framework.test import APITestCase
# Create your tests here.




class TestTask(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(first_name="user", last_name="1", email="user1@gmail.com",
                                             password="user1", username="user1")
        self.token=RefreshToken.for_user(self.user)
        self.access_token=self.token.access_token
        self.task=Task.objects.create(title='task1',description='task1',user=self.user)

    def test_new_task(self):
        data={
            "title":"task2",
            "description":"task2"
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response=self.client.post(reverse("new_task"),data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    def test_list_task(self):
        response = self.client.get(reverse("list_task"))
        self.assertEqual(response.status_code,status.HTTP_200_OK)


    def test_detail_task(self):

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get(reverse("detail_task",kwargs={"pk":self.task.pk}))
        self.assertEqual(response.status_code,status.HTTP_200_OK)


    def test_update_task(self):

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response= self.client.patch(reverse('update_task',kwargs={'pk':self.task.pk}),{"status":"Archived"})
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_completed_task(self):

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.post()