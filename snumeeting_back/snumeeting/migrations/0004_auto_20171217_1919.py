# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-12-17 10:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snumeeting', '0003_auto_20171216_1751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
