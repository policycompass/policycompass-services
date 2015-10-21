# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('referencepool', '0005_auto_20150603_1623'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='policydomain',
            options={'ordering': ['title'], 'verbose_name_plural': 'Policy Domains', 'verbose_name': 'Policy Domain'},
        ),
    ]
