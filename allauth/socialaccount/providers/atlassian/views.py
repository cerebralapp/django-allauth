from django.shortcuts import render

# Create your views here.
import requests

from allauth.socialaccount.providers.oauth2.views import (OAuth2Adapter,OAuth2LoginView, OAuth2CallbackView)

from .provider import AtlassianProvider


class AtlassianAuth2Adapter(OAuth2Adapter):
    provider_id = AtlassianProvider.id
    #access_token_url = 'https://example.com/applications/oauth2server/interface/oauth/token.php'
    access_token_url = 'https://auth.atlassian.com/oauth/token'
    #authorize_url = 'https://example.com/applications/oauth2server/interface/oauth/authorize.php'
    authorize_url = 'https://auth.atlassian.com/oauth/authorize'
    #profile_url = 'https://example.com/applications/oauth2server/interface/oauth/me.php'
    profile_url = 'https://auth.atlassian.com/api/2.0/users/me'

    # After successfully logging in, use access token to retrieve user info
    def complete_login(self, request, app, token, **kwargs):
        resp = requests.get(self.profile_url, params={'access_token': token.token})
        extra_data = resp.json()
        if app_settings.QUERY_EMAIL and not extra_data.get('email'):
            extra_data['email'] = self.get_email(token)
        return self.get_provider().sociallogin_from_response(request,extra_data)

oauth2_login = OAuth2LoginView.adapter_view(AtlassianAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(AtlassianAuth2Adapter)