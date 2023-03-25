from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class TestAdmin(TestCase):

    def test_login(self):
        response = self.client.get(reverse('admin:login'))
        self.assertEqual(response.status_code, 200)
        response.render()
        self.assertContains(response, reverse('social:begin', args=('auth0',)))

    def test_logged_in(self):
        user = User.objects.create_user('johndoe')
        user.is_staff = True
        user.set_password('welcome')
        user.save()
        self.client.login(username='johndoe', password='welcome')
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 200)
        response.render()
        self.assertContains(response, reverse('auth0_sso:logout'))
