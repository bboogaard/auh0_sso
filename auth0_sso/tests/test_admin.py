from unittest import mock

from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import RequestFactory
from django.urls import reverse

from auth0_sso.admin import Auth0UserRoleAdmin
from auth0_sso.models import Auth0UserRole


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


class TestAuth0UserRoleAdmin(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.site = AdminSite()
        self.user = User.objects.create_superuser('johndoe')

    @mock.patch('django.contrib.messages.add_message')
    @mock.patch('auth0_sso.client.Auth0Client.request')
    def test_sync_roles(self, mock_request, mock_message):
        mock_request.return_value = [
            {
                'id': 'rol_1',
                'name': 'admin_role',
                'description': 'An admin role'
            }
        ]
        admin = Auth0UserRoleAdmin(Auth0UserRole, self.site)
        request = RequestFactory().post("/", {'button_action': 'sync_roles'})
        request.user = self.user
        request._dont_enforce_csrf_checks = True
        response = admin.changelist_view(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Auth0UserRole.objects.filter(auth0_role_id='rol_1').exists())
