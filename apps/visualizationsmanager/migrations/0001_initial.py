# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ('metricsmanager','0001_initial'),
    ('eventsmanager','0001_initial'),
    ]

    operations = [ 
        migrations.CreateModel(
            name='VisualizationType',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Visualization Type',
                'verbose_name_plural': 'Visualizations Types',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Visualization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('keywords', models.CharField(blank=True, max_length=200)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('user_id', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),                
                ('updated_at', models.DateTimeField(blank=True)),
                ('publisher', models.CharField(blank=True, max_length=100)),
                ('views_count', models.IntegerField(blank=True, default=0)),
                #('visualization_type_id', models.IntegerField(blank=True, default=0)),
                ('visualization_type', models.ForeignKey(to='visualizationsmanager.VisualizationType')),
                ('language_id', models.IntegerField()),
                ('status_flag_id', models.IntegerField(blank=True, default=0)),
            ],
            options={
                'verbose_name': 'Visualization',
                'verbose_name_plural': 'Visualizations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MetricsInVisualizations',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('visualization', models.ForeignKey(to='visualizationsmanager.Visualization')),
                ('metric', models.ForeignKey(to='metricsmanager.Metric')),
                #('metric_id', models.IntegerField()),
                ('visualization_query', models.CharField(blank=True, max_length=100)),
                #('visualization', models.ForeignKey(to='visualizationsmanager.Visualization')),
                #('metric', models.ForeignKey(to='metricsmanager.Metric')),
            ],
            options={
                'verbose_name': 'Metric in Visualization',
                'verbose_name_plural': 'Metrics in Visualization',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HistoricalEventsInVisualizations',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('visualization', models.ForeignKey(to='visualizationsmanager.Visualization')),
                ('historical_event', models.ForeignKey(to='eventsmanager.HistoricalEvent')),
                #('historical_event_id', models.IntegerField()),                
                #('visualization', models.ForeignKey(to='visualizationsmanager.Visualization')),
                #('historical_events', models.ForeignKey(to='eventsmanager.HistoricalEvent')),
            ],
            options={
                'verbose_name': 'Historical event in Visualization',
                'verbose_name_plural': 'Historical events in Visualization',
            },
            bases=(models.Model,),
        ),
    ]