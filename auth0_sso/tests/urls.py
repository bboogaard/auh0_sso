from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('social_django.urls')),
    path('', include('auth0_sso.urls', namespace='auth0_sso')),
]
