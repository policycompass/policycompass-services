# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Indicator',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField()),
                ('language', models.IntegerField()),
                ('unit_category', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IndicatorInDomain',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('domain', models.IntegerField()),
                ('indicator', models.ForeignKey(to='indicatorservice.Indicator', related_name='policy_domains')),
            ],
            options={
                'verbose_name_plural': 'Indicators in Domains',
                'verbose_name': 'Indicator in Domain',
            },
            bases=(models.Model,),
        ),
    ]
