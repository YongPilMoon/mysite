# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-20 02:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0003_auto_20161020_0119'),
    ]

    operations = [
        migrations.RenameField(
            model_name='video',
            old_name='user',
            new_name='users',
        ),
    ]
