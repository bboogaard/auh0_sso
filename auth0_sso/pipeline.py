import logging

from .client import auth0_client, Auth0ClientException
from .signals import user_info_retrieved, user_roles_retrieved


logger = logging.getLogger(__name__)


def user_info_and_role(strategy, details, backend, uid, request, user=None, *args, **kwargs):
    """Retrieve user info. and user roles passed from the provider."""
    if not user:
        return

    provider = backend.name
    social = backend.strategy.storage.user.get_social_auth(provider, uid)
    if not social or social.user != user:
        return

    try:
        data = auth0_client.request('GET', f'/api/v2/users/{uid}')
        user_info_retrieved.send(user_info_and_role, uid=uid, user=user, user_info=data)
    except Auth0ClientException as exc:
        logger.error(str(exc))

    try:
        data = auth0_client.request('GET', f'/api/v2/users/{uid}/roles')
        user_roles_retrieved.send(user_info_and_role, uid=uid, user=user, roles=[role.get('name') for role in data])
    except Auth0ClientException as exc:
        logger.error(str(exc))
