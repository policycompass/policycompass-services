# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('referencepool', '0002_dateformat'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataClass',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(unique=True, max_length=100)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name': 'Class',
                'verbose_name_plural': 'Classes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Individual',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=100)),
                ('data_class', models.ForeignKey(to='referencepool.DataClass')),
            ],
            options={
                'verbose_name': 'Individual',
                'verbose_name_plural': 'Individuals',
            },
            bases=(models.Model,),
        ),
    ]
