# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def assign_spatial(apps, schema_editor):
    Event = apps.get_model("eventsmanager", "Event")
    Individual = apps.get_model("referencepool", "Individual")
    for event in Event.objects.all():
        if event.geoLocation is not None and isinstance(event.geoLocation, str):
            for individual in Individual.objects.all():
                if event.geoLocation == individual.title:
                   event.spatial = individual.id
                   event.save()


class Migration(migrations.Migration):

    dependencies = [
        ('eventsmanager', '0008_auto_20160419_0914'),
        ('referencepool', '0007_auto_20160107_1555'),
    ]

    operations = [
        migrations.RunPython(assign_spatial),
    ]
