# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datasetmanager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='metric_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='spatial',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
