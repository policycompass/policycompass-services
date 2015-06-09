# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indicatorservice', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indicator',
            name='indicators',
            field=models.ManyToManyField(to='indicatorservice.Indicator', related_name='indicators_rel_+', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='indicator',
            name='policy_domain',
            field=models.ForeignKey(null=True, to='referencepool.PolicyDomain', blank=True),
        ),
    ]
