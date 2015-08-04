# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations




class Migration(migrations.Migration):

    dependencies = [
        ('visualizationsmanager', '0003_auto_20140923_0949'),
    ]

    operations = [
        migrations.CreateModel(
            name='DatasetsInVisualizations',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('dataset_id', models.IntegerField()),
                ('visualization_query', models.CharField(max_length=800)),
                ('visualization', models.ForeignKey(related_name='datasets', to='visualizationsmanager.Visualization')),
            ],
            options={
                'verbose_name': 'Dataset in Visualization',
                'verbose_name_plural': 'Datasets in Visualization',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='metricsinvisualizations',
            name='visualization',
        ),
        migrations.DeleteModel(
            name='MetricsInVisualizations',
        ),
        migrations.AlterField(
            model_name='visualization',
            name='filter_configuration',
            field=models.CharField(max_length=800),
        ),
    ]
