import logging

from django.dispatch.dispatcher import receiver

from .signals import user_roles_retrieved


logger = logging.getLogger(__name__)


@receiver(user_roles_retrieved)
def map_admin_user(sender, uid, user, roles, **kwargs):
    from .models import Auth0UserRole

    auth0_roles = Auth0UserRole.objects.filter(auth0_role__in=roles)
    if any([auth0_role.is_staff for auth0_role in auth0_roles]):
        if not user.is_staff:
            # It's a staff user, give access to admin
            logger.info(f'User {uid} has admin role, granting admin access!!!')
            user.is_staff = True
            user.save()
    groups = set([group for auth0_role in auth0_roles for group in auth0_role.groups.all()])
    if groups:
        missing = [group for group in groups if group not in user.groups.all()]
        if missing:
            user.groups.add(*missing)
