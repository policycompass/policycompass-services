# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agmanager', '0003_argumentationgraph_is_draft'),
    ]

    operations = [
        migrations.RenameField(
            model_name='argumentationgraph',
            old_name='issued',
            new_name='date_created',
        ),
        migrations.RenameField(
            model_name='argumentationgraph',
            old_name='modified',
            new_name='date_modified',
        ),
    ]
