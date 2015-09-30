# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metricsmanager', '0002_auto_20150930_1314'),
    ]

    operations = [
        migrations.RenameField(
            model_name='metric',
            old_name='creator',
            new_name='creator_path',
        ),
        migrations.RenameField(
            model_name='metric',
            old_name='indicator',
            new_name='indicator_id',
        ),
    ]
