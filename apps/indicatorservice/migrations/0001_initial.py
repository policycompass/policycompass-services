# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('referencepool', '0005_auto_20150603_1623'),
    ]

    operations = [
        migrations.CreateModel(
            name='Indicator',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(unique=True, max_length=100)),
                ('description', models.TextField()),
                ('data_classes', models.ManyToManyField(to='referencepool.DataClass')),
                ('indicators', models.ManyToManyField(related_name='indicators_rel_+', blank=True, to='indicatorservice.Indicator')),
                ('policy_domain', models.ForeignKey(to='referencepool.PolicyDomain', blank=True)),
                ('units', models.ManyToManyField(to='referencepool.Unit')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
