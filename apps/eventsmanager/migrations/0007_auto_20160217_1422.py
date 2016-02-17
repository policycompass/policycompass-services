# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventsmanager', '0006_eventindomain'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eventindomain',
            options={'verbose_name': 'Event in Domain', 'verbose_name_plural': 'Event in Domains'},
        ),
    ]
