# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indicatorservice', '0007_auto_20160912_1156'),
    ]

    operations = [
        migrations.RenameField(
            model_name='indicator',
            old_name='issued',
            new_name='date_created',
        ),
        migrations.RenameField(
            model_name='indicator',
            old_name='modified',
            new_name='date_modified',
        ),
    ]
