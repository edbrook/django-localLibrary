from django.contrib import admin

from .models import *


class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'redirect_url', 'id', 'secret')

admin.site.register(Client, ClientAdmin)
