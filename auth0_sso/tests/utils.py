from typing import Dict, List, Optional, Union

from auth0_sso.client import Auth0ClientException
from social_django.models import UserSocialAuth


class Auth0TestClient:

    error: Optional[Auth0ClientException] = None

    response: Union[Dict, List]

    def setup(self, response: Union[Dict, List], error: Optional[Auth0ClientException] = None):
        self.response = response
        self.error = error

    def request(self, method: str, path: str, **kwargs) -> Union[Dict, List]:
        if self.error:
            raise self.error
        return self.response


auth0_test_client = Auth0TestClient()


class SocialTestUserMixin:

    user: Optional[UserSocialAuth]

    def get_social_auth(self, provider, uid):
        return self.user


class SocialTestStorage:

    user = SocialTestUserMixin()


class SocialTestStrategy:

    storage = SocialTestStorage()


class SocialTestBackend:

    name: str

    strategy = SocialTestStrategy()


def social_test_backend_factory(name: str, user: UserSocialAuth):
    backend = SocialTestBackend()
    setattr(backend, 'name', name)
    backend.strategy.storage.user.user = user
    return backend
