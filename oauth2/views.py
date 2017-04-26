from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from django.utils.crypto import get_random_string

from .forms import RegisterAppForm
from .models import *


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
