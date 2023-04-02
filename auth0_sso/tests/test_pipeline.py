import base64
from io import BytesIO
from unittest import mock

import requests
from django.contrib.auth.models import Group, User
from django.test import TestCase
from social_django.models import UserSocialAuth

from auth0_sso.client import Auth0ClientException
from auth0_sso.models import Auth0UserRole
from auth0_sso.pipeline import user_info_and_role
from .utils import social_test_backend_factory


@mock.patch.object(requests, 'get')
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
        self.img_data = b'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII='
        self.file = BytesIO()
        self.file.write(base64.b64decode(self.img_data))

    def test_user_info_and_role_with_groups(self, mock_request, mock_get):
        mock_request.side_effect = [
            {
                "created_at": "2023-03-20T11:10:15.234Z",
                "email": "johndoe@example.com",
                "email_verified": False,
                "name": "John Doe",
                "nickname": "johndoe",
                "picture": "https://avatar.png",
                "updated_at": "2023-03-28T20:14:57.390Z",
                "user_id": "auth0|asdf",
                "last_ip": "127.0.0.1",
                "last_login": "2023-03-28T20:14:57.390Z",
                "logins_count": 10
            },
            [{'name': 'tester'}],
        ]
        mock_response = mock.Mock(status_code=200)
        mock_response.content = self.file.getvalue()
        mock_get.return_value = mock_response

        user_info_and_role(self.backend.strategy, {}, self.backend, 'asdf', mock.Mock(), self.user)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_staff)
        self.assertTrue(self.group in self.user.groups.all())
        profile = self.user.auth0_user_profile
        self.assertEqual(profile.name, 'John Doe')
        img_data = base64.b64encode(profile.picture.open().read())
        self.assertEqual(img_data, self.img_data)

    def test_user_info_and_role_with_admin(self, mock_request, mock_get):
        mock_request.side_effect = [
            {
                "created_at": "2023-03-20T11:10:15.234Z",
                "email": "johndoe@example.com",
                "email_verified": False,
                "name": "John Doe",
                "nickname": "johndoe",
                "picture": "https://avatar.png",
                "updated_at": "2023-03-28T20:14:57.390Z",
                "user_id": "auth0|asdf",
                "last_ip": "127.0.0.1",
                "last_login": "2023-03-28T20:14:57.390Z",
                "logins_count": 10
            },
            [{'name': 'admin'}]
        ]
        mock_response = mock.Mock(status_code=200)
        mock_response.content = self.file.getvalue()
        mock_get.return_value = mock_response

        user_info_and_role(self.backend.strategy, {}, self.backend, 'asdf', mock.Mock(), self.user)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_staff)

    def test_no_user(self, mock_request, mock_get):
        user_info_and_role(self.backend.strategy, {}, self.backend, 'asdf', mock.Mock(), None)
        self.assertFalse(mock_request.called)

    def test_different_user(self, mock_request, mock_get):
        user = User.objects.create_user('janedoe')
        user_info_and_role(self.backend.strategy, {}, self.backend, 'asdf', mock.Mock(), user)
        self.assertFalse(mock_request.called)

    def test_with_error(self, mock_request, mock_get):
        mock_request.side_effect = Auth0ClientException()

        user_info_and_role(self.backend.strategy, {}, self.backend, 'asdf', mock.Mock(), self.user)
