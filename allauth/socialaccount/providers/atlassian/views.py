from django.shortcuts import render
import json

# Create your views here.
import requests

from allauth.socialaccount.providers.oauth2.views import (OAuth2Adapter,OAuth2LoginView, OAuth2CallbackView)

from .provider import AtlassianProvider

# class AtlassianOAuthAdapter(OAuthAdapter):
#     provider_id = AtlassianProvider.id
#     request_token_url = 'https://auth.atlassian.com/oauth/request_token'

#     #access_token_url = 'https://bitbucket.org/api/1.0/oauth/access_token'
#     access_token_url = 'https://auth.atlassian.com/oauth/token'
#     authorize_url = 'https://auth.atlassian.com/authorize'

#     def complete_login(self, request, app, token, **kwargs):
#         resp = requests.get(self.profile_url, params={'access_token': token.token})
#         extra_data = resp.json()['data']
#         return self.get_provider().sociallogin_from_response(request, extra_data)


class AtlassianAuth2Adapter(OAuth2Adapter):
    provider_id = AtlassianProvider.id
    #access_token_url = 'https://example.com/applications/oauth2server/interface/oauth/token.php'
    access_token_url = 'https://auth.atlassian.com/oauth/token'
    #access_token_url = 'https://api.atlassian.com/oauth2/token'
    #authorize_url = 'https://example.com/applications/oauth2server/interface/oauth/authorize.php'
    authorize_url = 'https://auth.atlassian.com/authorize/'
    accessible_resources_url = 'https://api.atlassian.com/oauth/token/accessible-resources'
    #authorize_url = 'https://api.atlassian.com/oauth2/authorize/'
    #profile_url = 'https://example.com/applications/oauth2server/interface/oauth/me.php'
    #profile_url = 'https://auth.atlassian.com/oauth/users/me'

    # After successfully logging in, use access token to retrieve user info
    def complete_login(self, request, app, token, **kwargs):
        print("token",token.token)
        access_token = "access_token "+token.token
        #resp = access_token.get(self.accessible_resources_url).body
        #header = {'Authorization': 'access_token token.token'}
        header = {'Authorization': 'Bearer %s' % token.token}
        resp = requests.get(self.accessible_resources_url, headers=header)
        #resp = requests.get(self.accessible_resources_url, params={'access_token': token.token})
        print("accessible_resources_url resp ****", resp)
        sites = resp.json()
        jira_user_scope = 'read:jira-user'
        print("sites******", sites)

        for site in sites:
            if jira_user_scope in site['scopes']:
                site_id = site['id']
                print("site_id", site_id)
        cloud_id = site_id
        base_url = "https://api.atlassian.com/ex/jira/#"+cloud_id
        myself_url = base_url+"/rest/api/3/myself"

        myself_resp = requests.get(self.myself_url, headers=header)

        extra_data=myself_resp.json()

        print("extra_data", extra_data)

        # resp = requests.get(self.profile_url, params={'access_token': token.token})
        # extra_data = resp.json()['data']
        return self.get_provider().sociallogin_from_response(request, extra_data)
        # extra_data = resp.json()
        # if app_settings.QUERY_EMAIL and not extra_data.get('email'):
        #     extra_data['email'] = self.get_email(token)
        # return self.get_provider().sociallogin_from_response(request,extra_data)

oauth2_login = OAuth2LoginView.adapter_view(AtlassianAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(AtlassianAuth2Adapter)

# oauth_login = OAuthLoginView.adapter_view(AtlassianOAuthAdapter)
# oauth_callback = OAuthCallbackView.adapter_view(AtlassianOAuthAdapter)
