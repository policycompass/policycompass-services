# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datasetmanager', '0003_auto_20151028_1559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='creator_path',
            field=models.CharField(max_length=1024),
        ),
    ]
