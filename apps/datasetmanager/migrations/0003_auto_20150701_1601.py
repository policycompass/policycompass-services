# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datasetmanager', '0002_auto_20150701_0847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='resource_id',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
