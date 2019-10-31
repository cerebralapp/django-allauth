from allauth.socialaccount.providers.oauth.urls import default_urlpatterns

from .provider import AtlassianProvider

urlpatterns = default_urlpatterns(AtlassianProvider)