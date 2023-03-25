from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class TestViews(TestCase):

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user('johndoe')
        self.user.set_password('welcome')
        self.user.save()

    def test_logout(self):
        self.client.login(username='johndoe', password='welcome')
        response = self.client.get(reverse('auth0_sso:logout'))
        self.assertEqual(response.status_code, 302)
