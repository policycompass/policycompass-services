# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExternalResource',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=100)),
                ('url', models.URLField()),
                ('api_url', models.URLField()),
            ],
            options={
                'verbose_name': 'External Resource',
                'verbose_name_plural': 'External Resources',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=2)),
                ('title', models.CharField(unique=True, max_length=100)),
            ],
            options={
                'verbose_name': 'Language',
                'verbose_name_plural': 'Languages',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PolicyDomain',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=100)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name': 'Policy Domain',
                'verbose_name_plural': 'Policy Domains',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=50)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name': 'Unit',
                'verbose_name_plural': 'Units',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UnitCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=100)),
            ],
            options={
                'verbose_name': 'Unit Category',
                'verbose_name_plural': 'Unit Categories',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='unit',
            name='unit_category',
            field=models.ForeignKey(to='referencepool.UnitCategory'),
            preserve_default=True,
        ),
    ]
