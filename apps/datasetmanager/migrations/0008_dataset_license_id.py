# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datasetmanager', '0007_auto_20160413_1512'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='license_id',
            field=models.IntegerField(blank=True, null=True),
            preserve_default=False,
        ),
    ]
