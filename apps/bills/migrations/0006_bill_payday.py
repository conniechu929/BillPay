# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-02 02:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0005_history'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='payday',
            field=models.IntegerField(default=22),
            preserve_default=False,
        ),
    ]
