# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PolicyDomain'
        db.create_table('referencepool_policydomain', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('referencepool', ['PolicyDomain'])

        # Adding model 'Language'
        db.create_table('referencepool_language', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=2)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
        ))
        db.send_create_signal('referencepool', ['Language'])

        # Adding model 'ExternalResource'
        db.create_table('referencepool_externalresource', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('api_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('referencepool', ['ExternalResource'])

        # Adding model 'UnitCategory'
        db.create_table('referencepool_unitcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
        ))
        db.send_create_signal('referencepool', ['UnitCategory'])

        # Adding model 'Unit'
        db.create_table('referencepool_unit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('unit_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['referencepool.UnitCategory'])),
        ))
        db.send_create_signal('referencepool', ['Unit'])


    def backwards(self, orm):
        # Deleting model 'PolicyDomain'
        db.delete_table('referencepool_policydomain')

        # Deleting model 'Language'
        db.delete_table('referencepool_language')

        # Deleting model 'ExternalResource'
        db.delete_table('referencepool_externalresource')

        # Deleting model 'UnitCategory'
        db.delete_table('referencepool_unitcategory')

        # Deleting model 'Unit'
        db.delete_table('referencepool_unit')


    models = {
        'referencepool.externalresource': {
            'Meta': {'object_name': 'ExternalResource'},
            'api_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'referencepool.language': {
            'Meta': {'object_name': 'Language'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'referencepool.policydomain': {
            'Meta': {'object_name': 'PolicyDomain'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'referencepool.unit': {
            'Meta': {'object_name': 'Unit'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'unit_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['referencepool.UnitCategory']"})
        },
        'referencepool.unitcategory': {
            'Meta': {'object_name': 'UnitCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        }
    }

    complete_apps = ['referencepool']