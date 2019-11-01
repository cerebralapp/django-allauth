from allauth.socialaccount import app_settings
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider
from allauth.socialaccount.providers.oauth.provider import OAuthProvider


class AtlassianAccount(ProviderAccount):
    pass
    # def get_profile_url(self):
    #     return self.account.extra_data.get('html_url')

    # def get_avatar_url(self):
    #     return self.account.extra_data.get('avatar_url')

    # def to_str(self):
    #     dflt = super(AtlassianAccount, self).to_str()
    #     return next(
    #         value
    #         for value in (
    #             self.account.extra_data.get('name', None),
    #             self.account.extra_data.get('email', None),
    #             dflt
    #         )
    #         if value is not None
    #     )


# class AtlassianProvider(OAuth2Provider):
#     id = 'atlassian'
#     name = 'Atlassian'
#     account_class = AtlassianAccount

#     def extract_uid(self, data):
#         return str(data['account_id'])

#     def extract_common_fields(self, data):
#         return dict(email=data.get('email'),
#                     name=data.get('name'))

class AtlassianProvider(OAuth2Provider):
    id = 'atlassian'
    name = 'Atlassian'
    account_class = AtlassianAccount

    def get_default_scope(self):
        scope = []
        if app_settings.QUERY_EMAIL:
            scope.append('user:email')
        return scope

    def extract_uid(self, data):
        return str(data['accountId'])

    def extract_common_fields(self, data):
        return dict(email=data.get('emailAddress'),
                    name=data.get('displayName'))


provider_classes = [AtlassianProvider]