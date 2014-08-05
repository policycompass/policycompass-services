# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalEventsInVisualizations',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('visualization', models.IntegerField()),
                ('historical_event', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MetricsInVisualizations',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('metric', models.IntegerField()),
                ('visualization', models.IntegerField()),
                ('visualization_query', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RawData',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('row', models.PositiveIntegerField()),
                ('value', models.FloatField()),
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
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
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
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
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
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('row', models.PositiveIntegerField()),
                ('value', models.CharField(max_length=200)),
                ('raw_data_extra', models.ForeignKey(to='visualizationsmanager.RawDataExtra')),
            ],
            options={
                'verbose_name': 'Raw Data Extra Data',
                'verbose_name_plural': 'Raw Data Extra Data',
                'ordering': ['row'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Visualization',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('keywords', models.CharField(blank=True, max_length=200)),
                ('publisher', models.CharField(blank=True, max_length=200)),
                ('user_id', models.IntegerField()),
                ('language_id', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('views_count', models.IntegerField()),
                ('visualization_type_id', models.IntegerField()),
                ('status_flag_id', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='rawdata',
            name='visualization',
            field=models.ForeignKey(to='visualizationsmanager.Visualization'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='VisualizationType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
