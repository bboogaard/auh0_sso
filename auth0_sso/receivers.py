import logging

from django.contrib.auth.models import Permission
from django.dispatch.dispatcher import receiver

from .settings import settings
from .signals import user_roles_retrieved


logger = logging.getLogger(__name__)


@receiver(user_roles_retrieved)
def map_admin_user(sender, uid, user, roles, **kwargs):
    if settings.ADMIN_ROLE in roles:
        if not user.is_staff:
            # It's a staff user, give access to admin
            logger.info(f'User {uid} has admin role, granting admin access!!!')
            user.is_staff = True
            user.save()
    if apps := settings.APP_PERMISSIONS:
        permissions = Permission.objects.filter(content_type__app_label__in=apps)
        missing = [permission for permission in permissions if permission not in user.user_permissions.all()]
        if missing:
            user.user_permissions.add(*missing)
