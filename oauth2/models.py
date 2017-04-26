import uuid

from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse


__all__ = ['Client', 'Token', 'AccessToken', 'RefreshToken', 'Scope']


class Client(models.Model):
    """Known OAuth2 applications"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    secret = models.CharField(max_length=200)
    redirect_url = models.CharField(max_length=200)
    user = models.ForeignKey(User)

    def get_absolute_url(self):
        return reverse('oauth2:client-detail', args=[str(self.id)])

    def __str__(self):
        return "{} ({})".format(self.name, self.id)


class Token(models.Model):
    """Access request tokens (single use)"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey('Client')
    user = models.ForeignKey(User)
    scope = models.CharField(max_length=100)
    expires = models.IntegerField()

    def __str__(self):
        return "{}".format(self.id)


class AccessToken(models.Model):
    """Token that OAuth2 client can use to access users account"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey('Client')
    user = models.ForeignKey(User)
    scope = models.CharField(max_length=100)
    expires = models.IntegerField()

    def __str__(self):
        return "{}".format(self.id)


class RefreshToken(models.Model):
    """Token OAuth2 client uses to get a new access token after it has expired"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey('Client')
    user = models.ForeignKey(User)
    scope = models.CharField(max_length=100)
    expires = models.IntegerField()

    def __str__(self):
        return "{}".format(self.id)


class Scope(models.Model):
    """Scopes that may be requested by the OAuth2 client"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20)

    def __str__(self):
        return "{}".format(self.name)
