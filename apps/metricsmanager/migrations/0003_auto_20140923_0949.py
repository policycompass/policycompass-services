# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metricsmanager', '0002_auto_20140915_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metricindomain',
            name='metric',
            field=models.ForeignKey(related_name='domains', to='metricsmanager.Metric'),
        ),
    ]
