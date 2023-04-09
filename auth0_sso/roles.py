import logging

from .client import auth0_client, Auth0ClientException
from .models import Auth0UserRole


logger = logging.getLogger(__name__)


def sync_roles() -> bool:
    try:
        data = auth0_client.request('GET', f'/api/v2/roles')
        for role in data:
            Auth0UserRole.objects.update_or_create(auth0_role=role['name'], defaults={
                'auth0_role_id': role['id'],
                'description': role['description']
            })
        return True
    except Auth0ClientException as exc:
        logger.error(str(exc))
        return False
