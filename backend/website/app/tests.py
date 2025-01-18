from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Task


# Create your tests here.
class TaskManagementTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser', password='testpassword')
        cls.token = RefreshToken.for_user(cls.user).access_token

    def setUp(self):
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def create_task(self, title='Test Task', description='Test Description', due_date='2023-12-31'):
        return Task.objects.create(owner_id=self.user, title=title, description=description, due_date=due_date)

    def test_create_task(self):
        url = reverse('create-task')
        data = {
            'title': 'Test Task',
            'description': 'Test Description',
            'due_date': '2023-12-31'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().title, 'Test Task')

    def test_get_task(self):
        task = self.create_task()
        url = reverse('manage-task', args=[task.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Task')

    def test_update_task(self):
        task = self.create_task()
        url = reverse('manage-task', args=[task.id])
        data = {'title': 'Updated Task'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.title, 'Updated Task')

    def test_delete_task(self):
        task = self.create_task()
        url = reverse('manage-task', args=[task.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.count(), 0)

    def test_manage_users(self):
        url = reverse('manage-users')
        data = {'type': 'default'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['username'], 'testuser')
