# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UnitCategory'
        db.create_table('metricsmanager_unitcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100, unique=True)),
        ))
        db.send_create_signal('metricsmanager', ['UnitCategory'])

        # Adding model 'Unit'
        db.create_table('metricsmanager_unit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50, unique=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('unit_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['metricsmanager.UnitCategory'])),
        ))
        db.send_create_signal('metricsmanager', ['Unit'])

        # Adding model 'Metric'
        db.create_table('metricsmanager_metric', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100, unique=True)),
            ('acronym', self.gf('django.db.models.fields.CharField')(max_length=20, unique=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('keywords', self.gf('django.db.models.fields.CharField')(max_length=400)),
            ('geo_location', self.gf('django.db.models.fields.CharField')(blank=True, max_length=1000)),
            ('publisher', self.gf('django.db.models.fields.CharField')(blank=True, max_length=200)),
            ('details_url', self.gf('django.db.models.fields.URLField')(blank=True, max_length=500)),
            ('license', self.gf('django.db.models.fields.CharField')(blank=True, max_length=100)),
            ('user_id', self.gf('django.db.models.fields.IntegerField')()),
            ('language_id', self.gf('django.db.models.fields.IntegerField')()),
            ('ext_resource_id', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('version', self.gf('django.db.models.fields.IntegerField')()),
            ('formula', self.gf('django.db.models.fields.CharField')(max_length=10000, default='1')),
            ('issued', self.gf('django.db.models.fields.DateField')()),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['metricsmanager.Unit'])),
        ))
        db.send_create_signal('metricsmanager', ['Metric'])

        # Adding model 'MetricInDomain'
        db.create_table('metricsmanager_metricindomain', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('domain_id', self.gf('django.db.models.fields.IntegerField')()),
            ('metric', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['metricsmanager.Metric'])),
        ))
        db.send_create_signal('metricsmanager', ['MetricInDomain'])

        # Adding model 'RawData'
        db.create_table('metricsmanager_rawdata', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('metric', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['metricsmanager.Metric'])),
            ('row', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('value', self.gf('django.db.models.fields.FloatField')()),
            ('from_date', self.gf('django.db.models.fields.DateField')()),
            ('to_date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('metricsmanager', ['RawData'])

        # Adding model 'RawDataCategory'
        db.create_table('metricsmanager_rawdatacategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100, unique=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('metricsmanager', ['RawDataCategory'])

        # Adding model 'RawDataExtra'
        db.create_table('metricsmanager_rawdataextra', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('metric', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['metricsmanager.Metric'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['metricsmanager.RawDataCategory'])),
        ))
        db.send_create_signal('metricsmanager', ['RawDataExtra'])

        # Adding model 'RawDataExtraData'
        db.create_table('metricsmanager_rawdataextradata', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('raw_data_extra', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['metricsmanager.RawDataExtra'])),
            ('row', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('metricsmanager', ['RawDataExtraData'])


    def backwards(self, orm):
        # Deleting model 'UnitCategory'
        db.delete_table('metricsmanager_unitcategory')

        # Deleting model 'Unit'
        db.delete_table('metricsmanager_unit')

        # Deleting model 'Metric'
        db.delete_table('metricsmanager_metric')

        # Deleting model 'MetricInDomain'
        db.delete_table('metricsmanager_metricindomain')

        # Deleting model 'RawData'
        db.delete_table('metricsmanager_rawdata')

        # Deleting model 'RawDataCategory'
        db.delete_table('metricsmanager_rawdatacategory')

        # Deleting model 'RawDataExtra'
        db.delete_table('metricsmanager_rawdataextra')

        # Deleting model 'RawDataExtraData'
        db.delete_table('metricsmanager_rawdataextradata')


    models = {
        'metricsmanager.metric': {
            'Meta': {'object_name': 'Metric'},
            'acronym': ('django.db.models.fields.CharField', [], {'max_length': '20', 'unique': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'details_url': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '500'}),
            'ext_resource_id': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'formula': ('django.db.models.fields.CharField', [], {'max_length': '10000', 'default': "'1'"}),
            'geo_location': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '1000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issued': ('django.db.models.fields.DateField', [], {}),
            'keywords': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'language_id': ('django.db.models.fields.IntegerField', [], {}),
            'license': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100'}),
            'publisher': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['metricsmanager.Unit']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user_id': ('django.db.models.fields.IntegerField', [], {}),
            'version': ('django.db.models.fields.IntegerField', [], {})
        },
        'metricsmanager.metricindomain': {
            'Meta': {'object_name': 'MetricInDomain'},
            'domain_id': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metric': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['metricsmanager.Metric']"})
        },
        'metricsmanager.rawdata': {
            'Meta': {'object_name': 'RawData', 'ordering': "['row']"},
            'from_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metric': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['metricsmanager.Metric']"}),
            'row': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'to_date': ('django.db.models.fields.DateField', [], {}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        'metricsmanager.rawdatacategory': {
            'Meta': {'object_name': 'RawDataCategory'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'})
        },
        'metricsmanager.rawdataextra': {
            'Meta': {'object_name': 'RawDataExtra'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['metricsmanager.RawDataCategory']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metric': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['metricsmanager.Metric']"})
        },
        'metricsmanager.rawdataextradata': {
            'Meta': {'object_name': 'RawDataExtraData', 'ordering': "['row']"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'raw_data_extra': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['metricsmanager.RawDataExtra']"}),
            'row': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'metricsmanager.unit': {
            'Meta': {'object_name': 'Unit'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50', 'unique': 'True'}),
            'unit_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['metricsmanager.UnitCategory']"})
        },
        'metricsmanager.unitcategory': {
            'Meta': {'object_name': 'UnitCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'})
        }
    }

    complete_apps = ['metricsmanager']