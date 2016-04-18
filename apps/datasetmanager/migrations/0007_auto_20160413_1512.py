# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def assign_spatial(apps, schema_editor):
    Dataset = apps.get_model("datasetmanager", "Dataset")
    DatasetInSpatial = apps.get_model("datasetmanager", "DatasetInSpatial")
    for dataset in Dataset.objects.all():
        if dataset.spatial is not None:
            d = DatasetInSpatial(spatial=dataset.spatial, dataset = dataset)
            d.save()


class Migration(migrations.Migration):
    dependencies = [
        ('datasetmanager', '0006_datasetinspatial'),
    ]

    operations = [
        migrations.RunPython(assign_spatial),
    ]
