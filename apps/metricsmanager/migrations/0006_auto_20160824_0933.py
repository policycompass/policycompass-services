# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('metricsmanager', '0005_remove_metric_acronym'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metric',
            name='variables',
            field=jsonfield.fields.JSONField(),
        ),
    ]
