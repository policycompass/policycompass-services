# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'UnitCategory'
        db.delete_table('metricsmanager_unitcategory')

        # Deleting model 'Unit'
        db.delete_table('metricsmanager_unit')

        # Deleting field 'Metric.unit'
        db.delete_column('metricsmanager_metric', 'unit_id')

        # Adding field 'Metric.unit_id'
        db.add_column('metricsmanager_metric', 'unit_id',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'UnitCategory'
        db.create_table('metricsmanager_unitcategory', (
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('metricsmanager', ['UnitCategory'])

        # Adding model 'Unit'
        db.create_table('metricsmanager_unit', (
            ('unit_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['metricsmanager.UnitCategory'])),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('metricsmanager', ['Unit'])

        # Adding field 'Metric.unit'
        db.add_column('metricsmanager_metric', 'unit',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['metricsmanager.Unit']),
                      keep_default=False)

        # Deleting field 'Metric.unit_id'
        db.delete_column('metricsmanager_metric', 'unit_id')


    models = {
        'metricsmanager.metric': {
            'Meta': {'object_name': 'Metric'},
            'acronym': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'details_url': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '500'}),
            'ext_resource_id': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'formula': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '10000'}),
            'geo_location': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '1000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issued': ('django.db.models.fields.DateField', [], {}),
            'keywords': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'language_id': ('django.db.models.fields.IntegerField', [], {}),
            'license': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100'}),
            'publisher': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'unit_id': ('django.db.models.fields.IntegerField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
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
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
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
        }
    }

    complete_apps = ['metricsmanager']