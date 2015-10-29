# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('indicatorservice', '0003_auto_20150715_0634'),
    ]

    operations = [
        migrations.AddField(
            model_name='indicator',
            name='creator_path',
            field=models.CharField(validators=[django.core.validators.RegexValidator('^(/[^/]*)+/?$')], max_length=1024, default='https://adhocracy-prod.policycompass.eu/api/principals/users/0000000/'),
            preserve_default=False,
        ),
    ]
