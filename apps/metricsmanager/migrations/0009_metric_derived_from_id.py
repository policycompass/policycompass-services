# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('metricsmanager', '0008_metric_date_modified'),
    ]

    operations = [
        migrations.AddField(
            model_name='metric',
            name='derived_from_id',
            field=models.ForeignKey(null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL, to='metricsmanager.Metric'),
            preserve_default=True,
        ),
    ]
