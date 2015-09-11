# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Metric',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('creator', models.IntegerField()),
                ('title', models.CharField(max_length=100, unique=True)),
                ('indicator', models.IntegerField()),
                ('formula', models.TextField()),
                ('variables', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
