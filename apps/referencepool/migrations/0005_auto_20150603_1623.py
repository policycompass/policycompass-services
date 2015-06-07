# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('referencepool', '0004_auto_20150603_1110'),
    ]

    operations = [
        migrations.AddField(
            model_name='unit',
            name='identifier',
            field=models.CharField(default='', unique=True, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='unitcategory',
            name='identifier',
            field=models.CharField(default='', unique=True, max_length=100),
            preserve_default=False,
        ),
    ]
