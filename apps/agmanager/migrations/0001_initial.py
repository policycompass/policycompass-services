# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import django.core.validators

from django.db import models, migrations

class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='ArgumentationGraph',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField()),
                ('data', models.TextField()),

                ('issued', models.DateTimeField(default=datetime.date(2016,1,18), auto_now_add=True)),
                ('modified', models.DateTimeField(default=datetime.date(2016,1,18), auto_now_add=True)),
                ('creator_path', models.CharField(validators=[django.core.validators.RegexValidator('^(/[^/]*)+/?$')], max_length=1024, default='https://adhocracy-prod.policycompass.eu/api/principals/users/0000000/')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
