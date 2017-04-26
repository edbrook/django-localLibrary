from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class RegisterAppForm(forms.Form):
    name = forms.CharField(max_length=200, label='Name of your app')
    redirect_url = forms.URLField(max_length=200, label='Redirect URL')

    def clean_redirect_url(self):
        data = self.cleaned_data['redirect_url']
        if not data.startswith('https://'):
            raise ValidationError(_('URLs must start with https://'))
        return data
