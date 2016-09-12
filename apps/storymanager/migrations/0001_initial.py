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
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=100, blank=True, default='')),
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
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('content', models.IntegerField()),
                ('story', models.ForeignKey(related_name='chapter_contents', to='storymanager.Chapter')),
            ],
            options={
                'verbose_name': 'Chapter in Content',
                'verbose_name_plural': 'Chapter in Contents',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
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
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(unique=True, max_length=100)),
                ('issued', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('creator_path', models.CharField(max_length=1024)),
                ('is_draft', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-issued'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StoryInChapter',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('chapter', models.IntegerField()),
                ('story', models.ForeignKey(related_name='story_chapters', to='storymanager.Story')),
            ],
            options={
                'verbose_name': 'Story in Chapter',
                'verbose_name_plural': 'Story in Chapters',
            },
            bases=(models.Model,),
        ),
    ]
