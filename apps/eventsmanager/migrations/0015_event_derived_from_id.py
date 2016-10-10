# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventsmanager', '0014_remove_event_viewscount'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='derived_from_id',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
