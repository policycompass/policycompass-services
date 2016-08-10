# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

import requests
import json

def assign_licenses(apps, schema_editor):
    License = apps.get_model("referencepool", "License")
    data = requests.get("http://licenses.opendefinition.org/licenses/groups/all.json")
    licenses = data.json()

    for key in licenses.keys():
        l = License(title=licenses[key]["title"], identifier=licenses[key]["id"], url=licenses[key]["url"])
        l.save()


class Migration(migrations.Migration):

    dependencies = [
        ('referencepool', '0008_license'),
    ]

    operations = [
        migrations.RunPython(assign_licenses),
    ]
