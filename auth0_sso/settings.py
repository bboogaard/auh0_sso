from django.conf import settings as django_settings


DEFAULTS = {
    'ADMIN_ROLE': 'django_admin'
}


class Settings:

    def __getattr__(self, item):
        return getattr(django_settings, f'AUTH0_SSO_{item}', DEFAULTS.get(item))


settings = Settings()
