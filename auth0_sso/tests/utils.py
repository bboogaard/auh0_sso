from typing import Optional

from social_django.models import UserSocialAuth


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
