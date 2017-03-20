# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-03-17 20:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0007_auto_20170210_0156'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='history',
            name='bill_id',
        ),
        migrations.AddField(
            model_name='history',
            name='amount',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='history',
            name='link',
            field=models.CharField(default='http//', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='history',
            name='title',
            field=models.CharField(default='title', max_length=200),
            preserve_default=False,
        ),
    ]