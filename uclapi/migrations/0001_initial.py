# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-05 00:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OAuthToken',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=80)),
            ],
        ),
    ]