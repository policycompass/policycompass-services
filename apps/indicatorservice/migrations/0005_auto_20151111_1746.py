# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indicatorservice', '0004_indicator_creator_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indicator',
            name='creator_path',
            field=models.CharField(max_length=1024),
        ),
    ]
