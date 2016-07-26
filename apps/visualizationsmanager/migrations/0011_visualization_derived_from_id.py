# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visualizationsmanager', '0010_visualization_is_draft'),
    ]

    operations = [
        migrations.AddField(
            model_name='visualization',
            name='derived_from_id',
            field=models.IntegerField(blank=True, null=True),
            preserve_default=True,
        ),
    ]
