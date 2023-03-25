from django.urls import path

from .views import logout


app_name = 'auth0_sso'


urlpatterns = [
    path('logout/auth0', logout, name='logout'),
]
