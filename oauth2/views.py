from urllib.parse import parse_qs, urlencode, urlsplit, urlunsplit
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from django.utils.crypto import get_random_string

from .forms import AuthorizeForm, RegisterAppForm
from .models import *


class AuthorizeView(LoginRequiredMixin, View):
    def get(self, req, *args, **kwargs):
        auth_req = AuthorizeForm(req.GET)
        if not auth_req.is_valid():
            return HttpResponseBadRequest('Invalid authorization request!')

        ctx = {
            'form': auth_req,
            'client': Client.objects.get(pk=auth_req.cleaned_data['client_id']),
            'scope': auth_req.cleaned_data['scope']
        }

        # Display the allow / deny page to the user
        return render(req, 'oauth2/authorize.html', ctx)

    def post(self, req, *args, **kwargs):
        auth_req = AuthorizeForm(req.POST)
        if not auth_req.is_valid():
            return HttpResponseBadRequest('Invalid authorization request!')
        # Create token
        now = datetime.now().timestamp()
        client = Client.objects.get(pk=auth_req.cleaned_data['client_id'])
        scope = Scope.objects.get(name=auth_req.cleaned_data['scope'])
        token = Token.objects.create(
            client=client,
            user=self.request.user,
            scope=scope,
            expires=now + 3600)
        url = auth_req.cleaned_data['redirect_url']
        scheme, netloc, path, qs, fragment = urlsplit(url)
        qs = parse_qs(qs)
        qs['code'] = token
        new_qs = urlencode(qs)
        url = urlunsplit((scheme, netloc, path, new_qs, fragment))
        return redirect(url)

# https://127.0.0.1:8000/oauth/authorize?
#   response_type=code          &
#   client_id=CLIENT_ID         &
#   redirect_uri=CALLBACK_URL   &
#   scope=read


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    paginate_by = 10
    context_object_name = 'client_list'

    def get_queryset(self):
        return Client.objects\
            .filter(user=self.request.user)\
            .order_by('name')


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client


class RegisterApp(LoginRequiredMixin, View):
    def get(self, req, *args, **kwargs):
        form = RegisterAppForm()
        return self._render_form(req, form)

    def post(self, req, *args, **kwargs):
        form = RegisterAppForm(req.POST)
        if form.is_valid():
            data = form.cleaned_data
            data['user'] = self.request.user
            data['secret'] = get_random_string(length=32)
            Client.objects.create(**data)
            return redirect('oauth2:client-list')
        return self._render_form(req, form)

    @staticmethod
    def _render_form(req, form):
        return render(req, 'catalog/forms/default_form.html', {
            'form': form,
            'operation': 'Register'})
