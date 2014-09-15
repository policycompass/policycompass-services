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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('historical_event_id', models.IntegerField()),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'verbose_name_plural': 'Historical Event in Visualization',
                'verbose_name': 'Historical Event in Visualization',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MetricsInVisualizations',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('metric_id', models.IntegerField()),
                ('visualization_query', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name_plural': 'Metrics in Visualization',
                'verbose_name': 'Metric in Visualization',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Visualization',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
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
                ('filter_configuration', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='metricsinvisualizations',
            name='visualization',
            field=models.ForeignKey(to='visualizationsmanager.Visualization'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='historicaleventsinvisualizations',
            name='visualization',
            field=models.ForeignKey(to='visualizationsmanager.Visualization'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='VisualizationType',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('type', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
