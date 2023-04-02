from django.template import Library

from ..models import Auth0UserProfile


register = Library()


@register.simple_tag(takes_context=True)
def auth0_user_info(context):
    try:
        user = getattr(context.get('request'), 'user')
    except AttributeError:
        return

    if not user or not user.is_authenticated:
        return

    try:
        profile = user.auth0_user_profile
        return {
            'name': profile.name,
            'picture': profile.picture.url
        }
    except Auth0UserProfile.DoesNotExist:
        ...
