# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventsmanager', '0011_auto_20160419_0936'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='is_draft',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
