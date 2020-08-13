from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_sample_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """creating user with valid payload"""
        payload = {
            'email': "someuser@test.com",
            'password': 'password0f1',
            'name': 'Iron Man'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertTrue(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exist(self):
        payload = {
            'email': "someuser@test.com",
            'password': 'password0f1',
            'name': 'Iron Man'
        }
        create_sample_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertTrue(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        payload = {
            'email': "something@test.com",
            'password': 'pw',
            'name': 'Iron Man'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertTrue(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exist = get_user_model().objects.filter(
            email=payload['email']).exists()

        self.assertFalse(user_exist)

    def test_create_token_forUser(self):
        payload = {
            'email': "new@test.com",
            'password': 'testpassword',
            'name': 'Iron Man'
        }

        create_sample_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        payload = {
            'email': "something@test.com",
            'password': 'testpassword',
            'name': 'Iron Man'}
        create_sample_user(**payload)
        payload['password'] = 'wrong_password'
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        payload = {
            'email': "idontexist@test.com",
            'password': 'somethingp',
            'name': 'Some guy'}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        payload = {
            'email': "other@test.com",
            # 'password': 'something',
            'name': 'Iron Man'}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_me_page_unauthorized(self):
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserAPITests(TestCase):
    """TEST API REQUEST THAT REQUIRES AUTHENTICATION"""

    def setUp(self):
        self.user = create_sample_user(
            email='test@test.com', password='password', name='test user')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'email': self.user.email,
            'name': self.user.name
        })

    def test_post_not_allowed(self):
        res = self.client.post(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        payload = {'name': 'new name', 'password': 'newpassword'}
        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
