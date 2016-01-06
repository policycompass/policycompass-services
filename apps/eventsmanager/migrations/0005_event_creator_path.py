# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventsmanager', '0004_auto_20151021_1316'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='creator_path',
            field=models.CharField(default='https://adhocracy-prod.policycompass.eu/api/principals/users/0000000/', max_length=1024),
            preserve_default=True,
        ),
    ]
