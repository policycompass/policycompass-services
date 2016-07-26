# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visualizationsmanager', '0011_visualization_derived_from_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visualization',
            name='description',
            field=models.TextField(),
        ),
    ]
