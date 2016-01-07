# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedbackmanager', '0002_auto_20160106_1642'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='link',
            field=models.CharField(blank=True, default='', max_length=1000),
            preserve_default=True,
        ),
    ]
