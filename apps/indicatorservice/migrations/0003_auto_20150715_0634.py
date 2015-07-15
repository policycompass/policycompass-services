# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('indicatorservice', '0002_indicator_acronym'),
    ]

    operations = [
        migrations.AddField(
            model_name='indicator',
            name='issued',
            field=models.DateTimeField(default=datetime.date(2015, 7, 15), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='indicator',
            name='modified',
            field=models.DateTimeField(default=datetime.date(2015, 7, 15), auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='indicatorindomain',
            name='indicator',
            field=models.ForeignKey(related_name='domains', to='indicatorservice.Indicator'),
        ),
    ]
