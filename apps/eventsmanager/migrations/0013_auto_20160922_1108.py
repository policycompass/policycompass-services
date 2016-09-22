# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventsmanager', '0012_event_is_draft'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='dateIssuedByExternalResource',
            new_name='date_created',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='dateModified',
            new_name='date_modified',
        ),
    ]
