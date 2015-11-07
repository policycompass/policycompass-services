# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('identifier', models.CharField(max_length=255, unique=True)),
                ('votes_counter', models.PositiveIntegerField(default=0)),
                ('score', models.DecimalField(decimal_places=1, max_digits=2, default=0.0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RatingVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('score', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('user_identifier', models.CharField(validators=[django.core.validators.RegexValidator('^(/[^/]*)+/?$')], max_length=1024)),
                ('timestamp_created', models.DateTimeField(auto_now_add=True)),
                ('timestamp_modified', models.DateTimeField(auto_now=True)),
                ('rating', models.ForeignKey(to='ratingsmanager.Rating', related_name='rating_votes')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='ratingvote',
            unique_together=set([('rating', 'user_identifier')]),
        ),
    ]
