# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visualizationsmanager', '0006_auto_20151023_1230'),
    ]

    operations = [
        migrations.AddField(
            model_name='visualization',
            name='location',
            field=models.IntegerField(blank=True, null=True),
            preserve_default=True,
        ),
    ]
