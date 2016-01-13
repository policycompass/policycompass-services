# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedbackmanager', '0004_feedback_issued'),
    ]

    operations = [
        migrations.RenameField(
            model_name='feedback',
            old_name='issued',
            new_name='date_created',
        ),
    ]
