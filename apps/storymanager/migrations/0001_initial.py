# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(default='', blank=True, max_length=100)),
                ('text', models.TextField()),
                ('number', models.IntegerField()),
                ('issued', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('creator_path', models.CharField(max_length=1024)),
            ],
            options={
                'ordering': ['-issued'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ChapterInContent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('content', models.IntegerField()),
                ('story', models.ForeignKey(to='storymanager.Chapter', related_name='chapter_contents')),
            ],
            options={
                'verbose_name_plural': 'Chapter in Contents',
                'verbose_name': 'Chapter in Content',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
                ('index', models.IntegerField()),
                ('issued', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('creator_path', models.CharField(max_length=1024)),
            ],
            options={
                'ordering': ['-issued'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(unique=True, max_length=100)),
                ('issued', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('creator_path', models.CharField(max_length=1024)),
            ],
            options={
                'ordering': ['-issued'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StoryInChapter',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('chapter', models.IntegerField()),
                ('story', models.ForeignKey(to='storymanager.Story', related_name='story_chapters')),
            ],
            options={
                'verbose_name_plural': 'Story in Chapters',
                'verbose_name': 'Story in Chapter',
            },
            bases=(models.Model,),
        ),
    ]
