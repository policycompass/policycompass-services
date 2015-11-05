# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'fki'

import json
from django.db import models, migrations
from ..models import Dataset
from ..dataset_data import *

def rewrite_data_field(apps, schema_editor):

    datasets = Dataset.objects.all()
    if datasets.exists():
        for d in datasets.iterator():
            old_data = json.loads(d.data)

            if 'data_frame' in old_data:
                print("Dataset " + str(d.pk) + " already updated. Nothing to do.")
            else:
                try:
                    data = DatasetDataTransformer.from_api(
                        old_data,
                        d.time_start,
                        d.time_end,
                        d.time_resolution,
                        d.class_id,
                        d.unit_id
                    )
                    d.data = data.get_json()
                    d.save()
                    print("Dataset " + str(d.pk) + " was updated.")
                except Exception as e:
                    print("Could not update Dataset " + str(d.pk) + ". Will be deleted")
                    d.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('datasetmanager', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(rewrite_data_field),
    ]