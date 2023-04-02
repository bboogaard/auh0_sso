import datetime
import logging

from django.dispatch.dispatcher import receiver
from django.utils.timezone import make_aware, utc

from .signals import user_info_retrieved, user_roles_retrieved
from .utils import save_image


logger = logging.getLogger(__name__)


@receiver(user_info_retrieved)
def map_user_info(sender, uid, user, user_info, **kwargs):
    from .models import Auth0UserProfile

    profile, _ = Auth0UserProfile.objects.update_or_create(
        user=user,
        defaults={
            'created_at': make_aware(datetime.datetime.fromisoformat(user_info['created_at'][:-1]), utc),
            'updated_at': make_aware(datetime.datetime.fromisoformat(user_info['updated_at'][:-1]), utc),
            'email': user_info['email'],
            'name': user_info['name'],
            'nickname': user_info['nickname']
        }
    )
    if image := save_image(user_info['picture']):
        profile.picture.save('profile.png', image)


@receiver(user_roles_retrieved)
def map_user_roles(sender, uid, user, roles, **kwargs):
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
