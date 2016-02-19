# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventsmanager', '0005_event_creator_path'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventInDomain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('domain', models.IntegerField()),
                ('event', models.ForeignKey(to='eventsmanager.Event', related_name='domains')),
            ],
            options={
                'verbose_name_plural': 'Events in Domains',
                'verbose_name': 'Event in Domain',
            },
            bases=(models.Model,),
        ),
    ]
