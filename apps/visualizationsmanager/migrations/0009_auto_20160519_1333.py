# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visualizationsmanager', '0008_visualizationindomain'),
    ]

    operations = [
        migrations.AddField(
            model_name='datasetsinvisualizations',
            name='scale',
            field=models.FloatField(null=True, default=None, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='datasetsinvisualizations',
            name='unit',
            field=models.CharField(max_length=200, null=True, default=None, blank=True),
            preserve_default=True,
        ),
    ]
