# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-19 16:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.EmailField(default=None, max_length=255),
            preserve_default=False,
        ),
    ]
