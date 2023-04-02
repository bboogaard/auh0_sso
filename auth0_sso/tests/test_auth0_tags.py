from django.contrib.auth.models import AnonymousUser, User
from django.template import Context, RequestContext, Template
from django.test import RequestFactory
from django.test.testcases import TestCase
from django.utils.timezone import now

from ..models import Auth0UserProfile


class TestAuth0Tags(TestCase):

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user('johndoe')
        current_time = now()
        Auth0UserProfile.objects.create(
            user=self.user, created_at=current_time, updated_at=current_time, name='John Doe', nickname='johndoe',
            email='johndoe@example.com', picture='avatar.png'
        )

    def render(self, value, **kwargs):
        request = kwargs.get('request')
        context = RequestContext(request, kwargs) if request else Context(kwargs)
        template = Template('{% load auth0_tags %}' + value)
        return template.render(context)

    def test_auth0_user_info(self):
        mock_request = RequestFactory().get('/')
        mock_request.user = self.user
        output = self.render(
            "{% auth0_user_info as user_info %}{% if user_info %}{{ user_info.name }} {{ user_info.picture }}"
            "{% endif %}",
            request=mock_request
        )
        self.assertEqual(output, 'John Doe /avatar.png')

    def test_auth0_user_info_no_user(self):
        mock_request = RequestFactory().get('/')
        output = self.render(
            "{% auth0_user_info as user_info %}{% if user_info %}{{ user_info.name }} {{ user_info.picture }}"
            "{% endif %}",
            request=mock_request
        )
        self.assertEqual(output, '')

    def test_auth0_user_info_anonymous_user(self):
        mock_request = RequestFactory().get('/')
        mock_request.user = AnonymousUser()
        output = self.render(
            "{% auth0_user_info as user_info %}{% if user_info %}{{ user_info.name }} {{ user_info.picture }}"
            "{% endif %}",
            request=mock_request
        )
        self.assertEqual(output, '')

    def test_auth0_user_info_no_profile(self):
        mock_request = RequestFactory().get('/')
        mock_request.user = User.objects.create_user('janedoe')
        output = self.render(
            "{% auth0_user_info as user_info %}{% if user_info %}{{ user_info.name }} {{ user_info.picture }}"
            "{% endif %}",
            request=mock_request
        )
        self.assertEqual(output, '')
