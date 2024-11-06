# Base imports
from typing import List

# Django imports
from django.urls import reverse

# Third party imports
from rest_framework import status
from model_bakery import baker

from authentication.models import User
# Project imports
from shared.tests import BaseAPITestCase


class HealthAuthView(BaseAPITestCase):
    """Test all scenarios for HealthAuthView."""

    tests_to_perform: List = []

    def setUp(self) -> None:
        super().setUp()
        self.url = reverse("health_auth")

    def test_health_200(self):
        response = self.client.get(f'{self.url}')
        self.assertEqual(status.HTTP_200_OK, response.status_code)


class UserCreateView(BaseAPITestCase):
    """Test all scenarios for HealthAuthView."""

    tests_to_perform: List = []

    def setUp(self) -> None:
        super().setUp()
        self.url = reverse("sign_up")

    def test_signup_201(self):
        response = self.client.post(
            f'{self.url}', data={
                'username': 'test',
                'email': 'test@test.com',
                'password': 'test@test',
            }
        )
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_signup_400(self):
        baker.make(
            'authentication.User',
            username='test',
            email='test@test.com',
        )
        response = self.client.post(
            f'{self.url}', data={
                'username': 'test',
                'password': 'test@test',
            }
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

        response = self.client.post(
            f'{self.url}', data={
                'email': 'test@test.com',
                'username': 'test',
                'password': 'test@test',
            }
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

        response = self.client.post(
            f'{self.url}', data={
                'email': 'test1@test.com',
                'username': 'test',
                'password': 'test@test',
            }
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_model_user(self):
        user = baker.make(
            'authentication.User'
        )
        self.assertEqual(str(user), user.__str__())

    def test_user_create_error(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(None, 'pass')

    def test_user_create_ok(self):
        user = User.objects.create_user('test@test.com', 'test@test')
        self.assertEqual(user.email, 'test@test.com')

    def test_user_create_superuser_error_super(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(email='test@example.com', password='password', is_superuser=False)

    def test_user_create_superuser_error_active(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(email='test@example.com', password='password', is_active=False)

    def test_user_create_superuser_error_staf(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(email='test@example.com', password='password', is_staff=False)

    def test_user_create_superuser_error_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(None, 'pass')

    def test_user_create_superuser_ok(self):
        user = User.objects.create_superuser('test@test.com', 'test@test')
        self.assertEqual(user.email, 'test@test.com')
