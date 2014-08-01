# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventsmanager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('keywords', models.CharField(max_length=200, blank=True)),
                ('startEventDate', models.DateTimeField(blank=True)),
                ('endEventDate', models.DateTimeField(blank=True)),
                ('detailsURL', models.URLField(max_length=500, blank=True)),
                ('geoLocation', models.CharField(max_length=1000, blank=True)),
                ('relatedVisualisation', models.CharField(max_length=200, blank=True)),
                ('languageID', models.IntegerField()),
                ('userID', models.IntegerField()),
                ('scale', models.CharField(max_length=200, blank=True)),
                ('externalResourceID', models.IntegerField(blank=True, default=0)),
                ('dateAddedToPC', models.DateTimeField(auto_now_add=True)),
                ('dateIssuedByExternalResource', models.DateTimeField(auto_now_add=True)),
                ('dateModified', models.DateTimeField(auto_now_add=True)),
                ('viewsCount', models.IntegerField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.DeleteModel(
            name='HistoricalEvent',
        ),
    ]
