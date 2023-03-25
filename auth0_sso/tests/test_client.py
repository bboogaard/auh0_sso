from unittest import mock

import requests
from django.test import SimpleTestCase

from auth0_sso.client import auth0_client, Auth0ClientException


@mock.patch.object(requests, 'request')
@mock.patch.object(requests, 'post')
class TestClient(SimpleTestCase):

    def test_request(self, mock_post, mock_request):
        mock_token_response = mock.Mock(status_code=200)
        mock_token_response.json.return_value = {
            'access_token': 'asdf'
        }
        mock_post.return_value = mock_token_response
        mock_response = mock.Mock(status_code=200)
        mock_response.json.return_value = [
            {
                'name': 'tester'
            }
        ]
        mock_request.return_value = mock_response
        auth0_client.request('GET', f'/api/v2/users/auth0|asdf/roles')

    def test_request_with_error(self, mock_post, mock_request):
        mock_token_response = mock.Mock(status_code=200)
        mock_token_response.json.return_value = {
            'access_token': 'asdf'
        }
        mock_post.return_value = mock_token_response
        mock_request.side_effect = requests.HTTPError()
        with self.assertRaises(Auth0ClientException):
            auth0_client.request('GET', f'/api/v2/users/auth0|asdf/roles')
