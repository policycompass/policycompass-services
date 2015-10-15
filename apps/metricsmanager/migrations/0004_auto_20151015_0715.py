# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import builtins
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('metricsmanager', '0003_auto_20150930_1427'),
    ]

    def create_valid_json(apps, schema_editor):
        Metric = apps.get_model("metricsmanager", "Metric")
        db_alias = schema_editor.connection.alias
        for metric in Metric.objects.using(db_alias).all():
            metric.variables = metric.variables.replace('\'','"')
            metric.save()

    operations = [
        migrations.RunPython(
            create_valid_json,
        ),
        migrations.AlterField(
            model_name='metric',
            name='variables',
            field=jsonfield.fields.JSONField(default=builtins.dict),
        ),
    ]
