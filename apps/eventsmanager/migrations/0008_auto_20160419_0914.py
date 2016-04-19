# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventsmanager', '0007_auto_20160217_1422'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='spatial',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
