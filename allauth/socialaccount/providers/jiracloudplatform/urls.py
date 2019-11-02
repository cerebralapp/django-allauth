from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from .provider import JiraCloudPlatformProvider

urlpatterns = default_urlpatterns(JiraCloudPlatformProvider)