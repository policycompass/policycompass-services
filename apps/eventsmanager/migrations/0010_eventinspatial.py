# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventsmanager', '0009_auto_20160419_0931'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventInSpatial',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('spatial', models.IntegerField()),
                ('event', models.ForeignKey(to='eventsmanager.Event', related_name='event_spatials')),
            ],
            options={
                'verbose_name_plural': 'Event in Spatials',
                'verbose_name': 'Event in Spatial',
            },
            bases=(models.Model,),
        ),
    ]
