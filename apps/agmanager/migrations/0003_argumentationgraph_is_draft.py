# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agmanager', '0002_auto_20160427_1033'),
    ]

    operations = [
        migrations.AddField(
            model_name='argumentationgraph',
            name='is_draft',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
