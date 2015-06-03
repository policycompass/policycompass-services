# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('referencepool', '0003_dataclass_individual'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataclass',
            name='code_type',
            field=models.CharField(blank=True, max_length=30, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='individual',
            name='code',
            field=models.CharField(blank=True, max_length=30, default=''),
            preserve_default=False,
        ),
    ]
