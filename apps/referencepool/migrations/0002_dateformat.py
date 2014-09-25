# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('referencepool', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DateFormat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('format', models.CharField(max_length=50, unique=True)),
                ('example', models.CharField(max_length=50)),
                ('symbol', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Date Formats',
                'verbose_name': 'Date Format',
            },
            bases=(models.Model,),
        ),
    ]
