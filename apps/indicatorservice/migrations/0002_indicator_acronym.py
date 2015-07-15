# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indicatorservice', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='indicator',
            name='acronym',
            field=models.CharField(default='NOTSET', max_length=20, unique=True),
            preserve_default=False,
        ),
    ]
