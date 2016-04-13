# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datasetmanager', '0005_remove_dataset_acronym'),
    ]

    operations = [
        migrations.CreateModel(
            name='DatasetInSpatial',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('spatial', models.IntegerField()),
                ('dataset', models.ForeignKey(related_name='dataset_spatials', to='datasetmanager.Dataset')),
            ],
            options={
                'verbose_name_plural': 'Dataset in Spatials',
                'verbose_name': 'Dataset in Spatial',
            },
            bases=(models.Model,),
        ),
    ]
