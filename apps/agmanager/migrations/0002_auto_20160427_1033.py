# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agmanager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='argumentationgraph',
            name='creator_path',
            field=models.CharField(max_length=1024),
        ),
        migrations.AlterField(
            model_name='argumentationgraph',
            name='issued',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='argumentationgraph',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
