# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-12-12 08:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snumeeting', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='meeting',
            name='tags',
            field=models.ManyToManyField(related_name='meetings_on_tag', to='snumeeting.Tag'),
        ),
    ]
