# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('storymanager', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chapter',
            options={'ordering': ['-date_created']},
        ),
        migrations.AlterModelOptions(
            name='content',
            options={'ordering': ['-date_created']},
        ),
        migrations.AlterModelOptions(
            name='story',
            options={'ordering': ['-date_created']},
        ),
        migrations.RenameField(
            model_name='chapter',
            old_name='issued',
            new_name='date_created',
        ),
        migrations.RenameField(
            model_name='chapter',
            old_name='modified',
            new_name='date_modified',
        ),
        migrations.RenameField(
            model_name='content',
            old_name='issued',
            new_name='date_created',
        ),
        migrations.RenameField(
            model_name='content',
            old_name='modified',
            new_name='date_modified',
        ),
        migrations.RenameField(
            model_name='story',
            old_name='issued',
            new_name='date_created',
        ),
        migrations.RenameField(
            model_name='story',
            old_name='modified',
            new_name='date_modified',
        ),
    ]
