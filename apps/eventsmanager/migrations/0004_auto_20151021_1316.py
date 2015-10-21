# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventsmanager', '0003_extractor_valid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='scale',
        ),
        migrations.AlterField(
            model_name='event',
            name='detailsURL',
            field=models.URLField(max_length=1000, blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='keywords',
            field=models.CharField(max_length=1000, blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='relatedVisualisation',
            field=models.CharField(max_length=1000, blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='title',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='extractor',
            name='name',
            field=models.CharField(max_length=1000),
        ),
    ]
