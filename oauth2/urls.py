from django.conf.urls import url
from .views import *

app_name = 'oauth2'

urlpatterns = [
    url(r'^apps/$', ClientListView.as_view(), name='client-list'),
    url(r'^apps/(?P<pk>[0-9a-zA-Z\-]{36})/', ClientDetailView.as_view(), name='client-detail'),
    url(r'^register/', RegisterApp.as_view(), name='register'),
    url(r'^authorize', AuthorizeView.as_view(), name='authorize'),
    # url(r'^token/', Token.as_view(), name='token'),
]
