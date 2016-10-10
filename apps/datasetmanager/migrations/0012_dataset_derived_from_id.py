# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datasetmanager', '0011_auto_20160922_1108'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='derived_from_id',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
