# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visualizationsmanager', '0009_auto_20160519_1333'),
    ]

    operations = [
        migrations.AddField(
            model_name='visualization',
            name='is_draft',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
