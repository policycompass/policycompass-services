# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('datasetmanager', '0002_dataframe'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dataset',
            name='user_id',
        ),
        migrations.AddField(
            model_name='dataset',
            name='creator_path',
            field=models.CharField(max_length=1024, validators=[django.core.validators.RegexValidator('^(/[^/]*)+/?$')], default='https://adhocracy-prod.policycompass.eu/api/principals/users/0000000/'),
            preserve_default=False,
        ),
    ]
