# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visualizationsmanager', '0004_auto_20150720_1057'),
    ]

    operations = [
        migrations.RenameField(
            model_name='visualization',
            old_name='user_id',
            new_name='creator_path',
        ),                  
    ]
