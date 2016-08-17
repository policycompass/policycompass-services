# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

class Migration(migrations.Migration):

    dependencies = [
        ('referencepool', '0007_auto_20160107_1555'),
    ]

    operations = [
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True)),
                ('identifier', models.CharField(max_length=100, unique=True)),
                ('url', models.URLField()),
            ],
            options={
                'ordering': ['title'],
                'verbose_name': 'License',
                'verbose_name_plural': 'Licenses',
            },
            bases=(models.Model,),
        ),
    ]
