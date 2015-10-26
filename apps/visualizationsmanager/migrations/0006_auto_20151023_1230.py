# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('visualizationsmanager', '0005_auto_20151023_0824'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='visualization',
            name='publisher',
        ),
        migrations.AlterField(
            model_name='visualization',
            name='creator_path',
            field=models.CharField(max_length=1024, validators=[django.core.validators.RegexValidator('^(/[^/]*)+/?$')]),
        ),
    ]
