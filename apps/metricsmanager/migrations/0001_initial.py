# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Metric',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=100)),
                ('acronym', models.CharField(unique=True, max_length=20)),
                ('description', models.TextField()),
                ('keywords', models.CharField(max_length=400)),
                ('geo_location', models.CharField(blank=True, max_length=1000)),
                ('publisher', models.CharField(blank=True, max_length=200)),
                ('details_url', models.URLField(blank=True, max_length=500)),
                ('publisher_issued', models.DateField(null=True, blank=True)),
                ('license', models.CharField(blank=True, max_length=100)),
                ('unit_id', models.IntegerField()),
                ('user_id', models.IntegerField()),
                ('language_id', models.IntegerField()),
                ('ext_resource_id', models.IntegerField(blank=True, default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('version', models.IntegerField(editable=False)),
                ('formula', models.CharField(max_length=10000, default='1')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MetricInDomain',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('domain_id', models.IntegerField()),
                ('metric', models.ForeignKey(to='metricsmanager.Metric')),
            ],
            options={
                'verbose_name': 'Metric in Domain',
                'verbose_name_plural': 'Metrics in Domains',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RawData',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('row', models.PositiveIntegerField()),
                ('value', models.FloatField()),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
                ('metric', models.ForeignKey(to='metricsmanager.Metric')),
            ],
            options={
                'verbose_name': 'Raw Data',
                'verbose_name_plural': 'Raw Data',
                'ordering': ['row'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RawDataCategory',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=100)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name': 'Raw Data Category',
                'verbose_name_plural': 'Raw Data Categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RawDataExtra',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('category', models.ForeignKey(to='metricsmanager.RawDataCategory')),
                ('metric', models.ForeignKey(to='metricsmanager.Metric')),
            ],
            options={
                'verbose_name': 'Raw Data Extra',
                'verbose_name_plural': 'Raw Data Extras',
                'ordering': ['id'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RawDataExtraData',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('row', models.PositiveIntegerField()),
                ('value', models.CharField(max_length=200)),
                ('raw_data_extra', models.ForeignKey(to='metricsmanager.RawDataExtra')),
            ],
            options={
                'verbose_name': 'Raw Data Extra Data',
                'verbose_name_plural': 'Raw Data Extra Data',
                'ordering': ['row'],
            },
            bases=(models.Model,),
        ),
    ]
