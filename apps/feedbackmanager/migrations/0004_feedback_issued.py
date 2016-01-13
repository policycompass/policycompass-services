# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('feedbackmanager', '0003_feedback_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='issued',
            field=models.DateTimeField(default=datetime.date(2016, 1, 13), auto_now_add=True),
            preserve_default=False,
        ),
    ]
