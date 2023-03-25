import logging

from .client import auth0_client, Auth0ClientException
from .signals import user_roles_retrieved


logger = logging.getLogger(__name__)


def user_role(strategy, details, backend, uid, request, user=None, *args, **kwargs):
    """Retrieve user roles passed from the provider."""
    if not user:
        return

    provider = backend.name
    social = backend.strategy.storage.user.get_social_auth(provider, uid)
    if not social or social.user != user:
        return

    try:
        data = auth0_client.request('GET', f'/api/v2/users/{uid}/roles')
        user_roles_retrieved.send(user_role, uid=uid, user=user, roles=[role.get('name') for role in data])
    except Auth0ClientException as exc:
        logger.error(str(exc))
