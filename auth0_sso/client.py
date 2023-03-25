import logging
from typing import Dict, List, Union

import requests
from django.conf import settings as django_settings
from requests.exceptions import RequestException, HTTPError, URLRequired


logger = logging.getLogger(__name__)


class Auth0ClientException(Exception):
    ...


class Auth0Client:

    audience: str

    base_url: str

    client_id: str

    client_secret: str

    domain: str

    def __init__(self):
        self.domain = django_settings.SOCIAL_AUTH_AUTH0_DOMAIN
        self.audience = f'https://{self.domain}/api/v2/'
        self.client_id = django_settings.SOCIAL_AUTH_AUTH0_KEY
        self.client_secret = django_settings.SOCIAL_AUTH_AUTH0_SECRET
        self.base_url = f"https://{self.domain}"

    def request(self, method: str, path: str, **kwargs) -> Union[Dict, List]:
        access_token = self.get_access_token()
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        try:
            response = requests.request(method, f'{self.base_url}{path}', headers=headers, **kwargs)
            return response.json()
        except (HTTPError, URLRequired, RequestException) as exc:
            raise Auth0ClientException(str(exc))

    def get_access_token(self) -> str:
        payload = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'audience': self.audience
        }
        response = requests.post(f'{self.base_url}/oauth/token', data=payload)
        oauth = response.json()
        return oauth.get('access_token')


auth0_client = Auth0Client()
