# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-05-24 23:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0007_auto_20180413_1052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='titles',
            field=models.TextField(default='', null=True),
        ),
        migrations.AlterField(
            model_name='lineitem',
            name='date',
            field=models.DateField(default='1990-01-01'),
        ),
        migrations.AlterField(
            model_name='lineitem',
            name='info',
            field=models.CharField(default='', max_length=200),
        ),
    ]
