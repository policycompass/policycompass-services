# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indicatorservice', '0006_remove_indicator_acronym'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='indicatorindomain',
            name='indicator',
        ),
        migrations.DeleteModel(
            name='IndicatorInDomain',
        ),
        migrations.RemoveField(
            model_name='indicator',
            name='language',
        ),
        migrations.RemoveField(
            model_name='indicator',
            name='unit_category',
        ),
    ]
