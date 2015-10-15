# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import builtins
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('metricsmanager', '0003_auto_20150930_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metric',
            name='variables',
            field=jsonfield.fields.JSONField(default=builtins.dict),
        ),
    ]
