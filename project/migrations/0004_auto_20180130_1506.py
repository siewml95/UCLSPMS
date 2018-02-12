# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-30 15:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_auto_20180120_2310'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='draft',
        ),
        migrations.AddField(
            model_name='project',
            name='status',
            field=models.IntegerField(choices=[(1, 'Draft'), (2, 'Active'), (3, 'Taken'), (4, 'Completed')], default=1),
        ),
    ]