# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('keywords', models.CharField(blank=True, max_length=200)),
                ('startEventDate', models.DateTimeField(blank=True)),
                ('endEventDate', models.DateTimeField(blank=True)),
                ('detailsURL', models.URLField(blank=True, max_length=500)),
                ('geoLocation', models.CharField(blank=True, max_length=1000)),
                ('relatedVisualisation', models.CharField(blank=True, max_length=200)),
                ('languageID', models.IntegerField()),
                ('userID', models.IntegerField()),
                ('scale', models.CharField(blank=True, max_length=200)),
                ('externalResourceID', models.IntegerField(default=0, blank=True)),
                ('dateAddedToPC', models.DateTimeField(auto_now_add=True)),
                ('dateIssuedByExternalResource', models.DateTimeField(auto_now_add=True)),
                ('dateModified', models.DateTimeField(auto_now_add=True)),
                ('viewsCount', models.IntegerField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
