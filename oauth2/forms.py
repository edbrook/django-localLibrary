from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist

from .models import *


class RegisterAppForm(forms.Form):
    name = forms.CharField(max_length=200, label='Name of your app')
    redirect_url = forms.URLField(max_length=200, label='Redirect URL')

    def clean_redirect_url(self):
        data = self.cleaned_data.get('redirect_url')
        if not data.startswith('https://'):
            raise ValidationError(_('URLs must start with https://'))
        return data


class AuthorizeForm(forms.Form):
    oauth_res_types = (('code', 'Authorization Code'),)
    response_type = forms.ChoiceField(choices=oauth_res_types, widget=forms.HiddenInput)
    client_id = forms.UUIDField(widget=forms.HiddenInput)
    redirect_url = forms.URLField(widget=forms.HiddenInput)
    scope = forms.CharField(max_length=20, widget=forms.HiddenInput)

    def clean(self):
        clid = self.cleaned_data.get('client_id')
        url = self.cleaned_data.get('redirect_url')
        scope = self.cleaned_data.get('scope')
        try:
            client = Client.objects.get(pk=clid)
        except (ValueError, ObjectDoesNotExist):
            raise ValidationError(_('Invalid client ID!'))

        errors = False
        if not url.startswith(client.redirect_url):
            errors = True
        if not errors and Scope.objects.filter(name=scope).count() == 0:
            errors = True

        if errors:
            raise ValidationError(_('Invalid authorization request'))
        return self.cleaned_data
