# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.apps import apps as django_apps

def assign_license(apps, schema_editor):
    Dataset = apps.get_model("datasetmanager", "Dataset")
    License = django_apps.get_model("referencepool", "License")
    licenses_list = License.objects.all()
    for dataset in Dataset.objects.all():
        if len(dataset.license) > 0:
            for license in licenses_list:
                if dataset.license == license.title or dataset.license == license.identifier or dataset.license == license.url:
                    dataset.license_id = license.id
                    dataset.save()


class Migration(migrations.Migration):

    dependencies = [
        ('datasetmanager', '0008_dataset_license_id'),
    ]

    operations = [
        migrations.RunPython(assign_license),
    ]
