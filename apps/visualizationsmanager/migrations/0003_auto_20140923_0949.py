# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visualizationsmanager', '0002_historicaleventsinvisualizations_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicaleventsinvisualizations',
            name='visualization',
            field=models.ForeignKey(related_name='historical_events', to='visualizationsmanager.Visualization'),
        ),
        migrations.AlterField(
            model_name='metricsinvisualizations',
            name='visualization',
            field=models.ForeignKey(related_name='metrics', to='visualizationsmanager.Visualization'),
        ),
    ]
