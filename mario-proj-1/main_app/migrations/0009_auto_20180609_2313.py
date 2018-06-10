# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-06-09 23:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_app', '0008_auto_20180524_1653'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='category',
            unique_together=set([('user', 'name')]),
        ),
    ]