# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('metricsmanager', '0007_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='metric',
            name='date_modified',
            field=models.DateTimeField(auto_now=True, default=datetime.date(2016, 9, 22)),
            preserve_default=False,
        ),
    ]
