# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visualizationsmanager', '0012_auto_20160726_1208'),
    ]

    operations = [
        migrations.RenameField(
            model_name='visualization',
            old_name='created_at',
            new_name='date_created',
        ),
        migrations.RenameField(
            model_name='visualization',
            old_name='updated_at',
            new_name='date_modified',
        ),
        migrations.RemoveField(
            model_name='visualization',
            name='views_count',
        ),
    ]
