# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-14 17:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='address',
            field=models.TextField(verbose_name='Address'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='mobile',
            field=models.CharField(default='9876543210', max_length=11, verbose_name='Mobile Number'),
        ),
    ]
