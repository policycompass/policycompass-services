# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=100, unique=True)),
                ('acronym', models.CharField(max_length=20, unique=True)),
                ('description', models.TextField()),
                ('keywords', models.CharField(max_length=400)),
                ('resource_url', models.URLField(max_length=500, blank=True)),
                ('resource_issued', models.DateField(blank=True)),
                ('resource_id', models.IntegerField(null=True, blank=True)),
                ('resource_publisher', models.CharField(max_length=100, blank=True)),
                ('is_applied', models.BooleanField(default=False)),
                ('metric_id', models.IntegerField(null=True, blank=True)),
                ('spatial', models.IntegerField(null=True, blank=True)),
                ('license', models.CharField(max_length=100, blank=True)),
                ('version', models.IntegerField(editable=False)),
                ('time_resolution', models.CharField(max_length=10, choices=[('year', 'Year'), ('month', 'Month'), ('day', 'Day'), ('decade', 'Decade'), ('quarter', 'Quarter')])),
                ('time_start', models.CharField(max_length=20)),
                ('time_end', models.CharField(max_length=20)),
                ('language_id', models.IntegerField()),
                ('user_id', models.IntegerField()),
                ('unit_id', models.IntegerField()),
                ('indicator_id', models.IntegerField()),
                ('class_id', models.IntegerField()),
                ('issued', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('data', models.TextField()),
            ],
            options={
                'ordering': ['-issued'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DatasetInDomain',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('domain', models.IntegerField()),
                ('dataset', models.ForeignKey(to='datasetmanager.Dataset', related_name='domains')),
            ],
            options={
                'verbose_name': 'Dataset in Domain',
                'verbose_name_plural': 'Dataset in Domains',
            },
            bases=(models.Model,),
        ),
    ]
