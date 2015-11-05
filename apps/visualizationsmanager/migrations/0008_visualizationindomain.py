# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visualizationsmanager', '0007_visualization_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='VisualizationInDomain',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('domain', models.IntegerField()),
                ('visualization', models.ForeignKey(to='visualizationsmanager.Visualization', related_name='domains')),
            ],
            options={
                'verbose_name_plural': 'Visualization in Domains',
                'verbose_name': 'Visualization in Domain',
            },
            bases=(models.Model,),
        ),
    ]
