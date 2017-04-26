from django.conf.urls import url

app_name = 'oauth2'

from .views import *

urlpatterns = [
    # url(r'^authorise/', Authorise.as_view(), name='authorise'),
    # url(r'^token/', Token.as_view(), name='token'),
    url(r'^apps/$', ClientListView.as_view(), name='client-list'),
    url(r'^apps/(?P<pk>[0-9a-zA-Z\-]{36})/', ClientDetailView.as_view(), name='client-detail'),
    url(r'^register/', RegisterApp.as_view(), name='register'),
]
