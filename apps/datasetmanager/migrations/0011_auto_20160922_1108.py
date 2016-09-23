# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datasetmanager', '0010_dataset_is_draft'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dataset',
            options={'ordering': ['-date_created']},
        ),
        migrations.RenameField(
            model_name='dataset',
            old_name='issued',
            new_name='date_created',
        ),
        migrations.RenameField(
            model_name='dataset',
            old_name='modified',
            new_name='date_modified',
        ),
    ]
