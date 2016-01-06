# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedbackmanager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='comment',
            field=models.TextField(default=' '),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='feedback',
            name='email',
            field=models.CharField(max_length=100, default=' '),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='name',
            field=models.CharField(max_length=100, default=' '),
        ),
    ]
