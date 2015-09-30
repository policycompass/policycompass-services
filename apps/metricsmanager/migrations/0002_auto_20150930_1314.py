# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators

import random
import string

class Migration(migrations.Migration):

    dependencies = [
        ('metricsmanager', '0001_initial'),
    ]

    def set_random_acronym(apps, schema_editor):
        Metric = apps.get_model("metricsmanager", "Metric")
        db_alias = schema_editor.connection.alias
        for metric in Metric.objects.using(db_alias).filter(acronym="NOTSET"):
            metric.acronym = ''.join([random.choice(string.ascii_letters + string.digits) for x in range(20)])
            metric.save()

    def migrate_creator(apps, schema_editor):
        Metric = apps.get_model("metricsmanager", "Metric")
        db_alias = schema_editor.connection.alias
        for metric in Metric.objects.using(db_alias).all():
            try:
                user_id = int(metric.creator)
                metric.creator = "/principals/users/%07d" % user_id
                metric.save()
            except ValueError:
                pass # was already a path

    operations = [
        migrations.AddField(
             model_name='metric',
             name='acronym',
             field=models.CharField(default="NOTSET", max_length=20),
             preserve_default=False,
        ),
        migrations.RunPython(
            set_random_acronym,
        ),
        migrations.AlterField(
             model_name='metric',
             name='acronym',
             field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AddField(
            model_name='metric',
            name='description',
            field=models.TextField(default='', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='metric',
            name='keywords',
            field=models.CharField(default='', blank=True, max_length=400, validators=[django.core.validators.RegexValidator('^([_\\-a-zA-Z0-9]+ ?($|,))+')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='metric',
            name='creator',
            field=models.CharField( max_length=1024, validators=[django.core.validators.RegexValidator('^(/[^/]*)+/?$')]),
        ),
        migrations.RunPython(
            migrate_creator,
        ),
    ]
