# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metricsmanager', '0004_auto_20151015_0715'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='metric',
            name='acronym',
        ),
    ]
