# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metricsmanager', '0005_remove_metric_acronym'),
    ]

    operations = [
        migrations.AddField(
            model_name='metric',
            name='is_draft',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
