# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def assign_spatial(apps, schema_editor):
    Event = apps.get_model("eventsmanager", "Event")
    EventInSpatial = apps.get_model("eventsmanager", "EventInSpatial")
    for event in Event.objects.all():
        if event.spatial is not None:
            e = EventInSpatial(spatial=event.spatial, event = event)
            e.save()


class Migration(migrations.Migration):

    dependencies = [
        ('eventsmanager', '0010_eventinspatial'),
    ]

    operations = [
        migrations.RunPython(assign_spatial),
    ]
