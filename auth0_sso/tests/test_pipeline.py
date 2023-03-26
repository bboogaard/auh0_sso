from unittest import mock

from django.contrib.auth.models import Group, User
from django.test import TestCase
from social_django.models import UserSocialAuth

from auth0_sso.client import Auth0ClientException
from auth0_sso.models import Auth0UserRole
from auth0_sso.pipeline import user_role
from .utils import social_test_backend_factory


@mock.patch('auth0_sso.client.Auth0Client.request')
class TestPipeline(TestCase):

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user('johndoe')
        self.group = Group.objects.create(name='testers')
        auth0_user_role = Auth0UserRole.objects.create(auth0_role='tester')
        auth0_user_role.groups.add(self.group)
        Auth0UserRole.objects.create(auth0_role='admin', is_staff=True)
        self.auth_user = UserSocialAuth.objects.create(provider='auth0', uid='asdf', user=self.user)
        self.backend = social_test_backend_factory('auth0', self.auth_user)

    def test_role_with_groups(self, mock_request):
        mock_request.return_value = [{'name': 'tester'}]

        user_role(self.backend.strategy, {}, self.backend, 'asdf', mock.Mock(), self.user)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_staff)
        self.assertTrue(self.group in self.user.groups.all())

    def test_role_with_admin(self, mock_request):
        mock_request.return_value = [{'name': 'admin'}]

        user_role(self.backend.strategy, {}, self.backend, 'asdf', mock.Mock(), self.user)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_staff)

    def test_no_user(self, mock_request):
        user_role(self.backend.strategy, {}, self.backend, 'asdf', mock.Mock(), None)
        self.assertFalse(mock_request.called)

    def test_different_user(self, mock_request):
        user = User.objects.create_user('janedoe')
        user_role(self.backend.strategy, {}, self.backend, 'asdf', mock.Mock(), user)
        self.assertFalse(mock_request.called)

    def test_with_error(self, mock_request):
        mock_request.side_effect = Auth0ClientException()

        user_role(self.backend.strategy, {}, self.backend, 'asdf', mock.Mock(), self.user)
