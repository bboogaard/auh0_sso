# auth0-sso

Auth0 SSO for Django with role mapping

## Rationale

Log in to Auth0 and map users and roles to Django users.

## Support

Supports: Python 3.9.

Supports Django Versions: 3.2.

## Installation

```shell
$ pip install ...
```

## Usage

Add `auth0_sso` and `social_django` to `INSTALLED_APPS` before `django.contrib.admin`, then add these settings to set
up the auth0 connection::

```python
import environ

env = environ.Env()

SOCIAL_AUTH_AUTH0_DOMAIN = env.str('SOCIAL_AUTH_AUTH0_DOMAIN', 'dev')
SOCIAL_AUTH_AUTH0_KEY = env.str('SOCIAL_AUTH_AUTH0_KEY', 'dev')
SOCIAL_AUTH_AUTH0_SECRET = env.str('SOCIAL_AUTH_AUTH0_SECRET', 'dev')
SOCIAL_AUTH_AUTH0_SCOPE = [
    'openid',
    'profile',
    'email'
]
SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'auth0_sso.pipeline.user_role'
)

AUTHENTICATION_BACKENDS = {
    'social_core.backends.auth0.Auth0OAuth2',
    'django.contrib.auth.backends.ModelBackend'
}

LOGIN_URL = '/login/auth0/'
LOGIN_REDIRECT_URL = '/admin/'
LOGOUT_REDIRECT_URL = '/admin/login/'
```

Add additional settings for mapping roles and permissions:

```python
AUTH0_SSO_ADMIN_ROLE = 'my_admin_role'
AUTH0_SSO_APP_PERMISSIONS = ['myapp']
```
