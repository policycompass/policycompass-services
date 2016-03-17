# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indicatorservice', '0005_auto_20151111_1746'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='indicator',
            name='acronym',
        ),
    ]
