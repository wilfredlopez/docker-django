from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTest(TestCase):

    def test_create_user_with_email_successful(self):
        email = 'test@test.com'
        password = 'password'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        email = 'test@TESTING.com'
        password = 'password'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalidEmail(self):
        email = ''
        password = 'password'
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=email,
                password=password
            )

    def test_create_superuser(self):
        "Test creating a new super user"
        user = get_user_model().objects.create_superuser('admin@test.com', 'password')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
