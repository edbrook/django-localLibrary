# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-27 15:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_auto_20170126_1559'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['status', 'due_back'], 'permissions': (('can_mark_returned', 'Set book as returned'),)},
        ),
    ]
