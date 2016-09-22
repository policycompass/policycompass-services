# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventsmanager', '0013_auto_20160922_1108'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='viewsCount',
        ),
    ]
