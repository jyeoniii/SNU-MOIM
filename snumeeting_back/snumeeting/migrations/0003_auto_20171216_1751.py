# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-12-16 08:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('snumeeting', '0002_auto_20171212_0830'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.localtime),
        ),
        migrations.AddField(
            model_name='meeting',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.localtime),
        ),
    ]
