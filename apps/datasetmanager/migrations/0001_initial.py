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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, unique=True)),
                ('acronym', models.CharField(max_length=20, unique=True)),
                ('description', models.TextField()),
                ('keywords', models.CharField(max_length=400)),
                ('resource_url', models.URLField(blank=True, max_length=500)),
                ('resource_issued', models.DateField(blank=True)),
                ('resource_id', models.IntegerField(blank=True)),
                ('resource_publisher', models.CharField(blank=True, max_length=100)),
                ('is_applied', models.BooleanField(default=False)),
                ('metric_id', models.IntegerField(blank=True)),
                ('spatial', models.IntegerField(blank=True)),
                ('license', models.CharField(blank=True, max_length=100)),
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
            ],
            options={
                'ordering': ['-issued'],
            },
            bases=(models.Model,),
        ),
    ]
