# myapp/tests.py
from django.core import mail
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User


class UserRegistrationTest(APITestCase):
    def test_user_registration(self):
        url = reverse('user-register')
        data = {'username': 'testuser', 'password': 'password',
                'email': 'test@example.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class AnimalAPITest(APITestCase):
    def test_create_animal(self):
        url = reverse('animal-list')
        data = {'name': 'Max', 'age': 5,
                'animal_type': 'dog', 'breed': 'Bulldog'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class UserViewSetTests(APITestCase):

    def test_send_email(self):
        """Test sending an email using the send_email action"""
        url = reverse(
            'user-send-email')  # Adjust this to your URL name for the send_email action

        # Send POST request to send email
        response = self.client.post(url, {
            'email': 'testuser@example.com',
            'subject': 'Test Subject',
            'message': 'This is a test message.',
        })

        # Assert success response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'Email sent successfully!')

        # Check if the email was actually sent
        self.assertEqual(len(mail.outbox), 1)  # Check if one email was sent
        self.assertEqual(mail.outbox[0].subject, 'Test Subject')
        self.assertEqual(mail.outbox[0].to, ['testuser@example.com'])
        self.assertEqual(mail.outbox[0].body, 'This is a test message.')

    def test_send_email_missing_email(self):
        """Test sending email without an email address"""
        url = reverse('user-send-email')

        response = self.client.post(url, {
            'subject': 'Test Subject',
            'message': 'This is a test message without an email.',
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Email is required')

    def test_send_email_failed(self):
        """Test sending email with incorrect configuration (e.g., invalid SMTP settings)"""
        url = reverse('user-send-email')

        # Invalid email to simulate error
        response = self.client.post(url, {
            'email': 'invalid-email',
            'subject': 'Test Subject',
            'message': 'This will fail.',
        })

        self.assertEqual(response.status_code,
                         status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn('Failed to send email', response.data['error'])
