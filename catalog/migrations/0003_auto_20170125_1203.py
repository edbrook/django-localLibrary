# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-25 12:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20170125_1156'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='language',
            options={'ordering': ['name']},
        ),
    ]
