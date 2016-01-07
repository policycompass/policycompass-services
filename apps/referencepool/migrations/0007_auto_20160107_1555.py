# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('referencepool', '0006_auto_20151021_1308'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dataclass',
            options={'verbose_name_plural': 'Classes', 'verbose_name': 'Class', 'ordering': ['title']},
        ),
        migrations.AlterModelOptions(
            name='externalresource',
            options={'verbose_name_plural': 'External Resources', 'verbose_name': 'External Resource', 'ordering': ['title']},
        ),
        migrations.AlterModelOptions(
            name='individual',
            options={'verbose_name_plural': 'Individuals', 'verbose_name': 'Individual', 'ordering': ['title']},
        ),
        migrations.AlterModelOptions(
            name='language',
            options={'verbose_name_plural': 'Languages', 'verbose_name': 'Language', 'ordering': ['title']},
        ),
        migrations.AlterModelOptions(
            name='unit',
            options={'verbose_name_plural': 'Units', 'verbose_name': 'Unit', 'ordering': ['title']},
        ),
        migrations.AlterModelOptions(
            name='unitcategory',
            options={'verbose_name_plural': 'Unit Categories', 'verbose_name': 'Unit Category', 'ordering': ['title']},
        ),
    ]
