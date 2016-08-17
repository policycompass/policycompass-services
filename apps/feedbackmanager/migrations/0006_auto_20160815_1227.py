# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedbackmanager', '0005_auto_20160113_1248'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeedbackCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Feedback Categories',
                'ordering': ['title'],
                'verbose_name': 'Feedback Category',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='feedback',
            name='category_id',
            field=models.IntegerField(blank=True, null=True),
            preserve_default=True,
        ),
    ]
