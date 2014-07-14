# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Metric.publisher_issued'
        db.alter_column('metricsmanager_metric', 'publisher_issued', self.gf('django.db.models.fields.DateField')(null=True))

    def backwards(self, orm):

        # Changing field 'Metric.publisher_issued'
        db.alter_column('metricsmanager_metric', 'publisher_issued', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2014, 7, 14, 0, 0)))

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
            'keywords': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'language_id': ('django.db.models.fields.IntegerField', [], {}),
            'license': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100'}),
            'publisher': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '200'}),
            'publisher_issued': ('django.db.models.fields.DateField', [], {'blank': 'True', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'}),
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
            'Meta': {'ordering': "['row']", 'object_name': 'RawData'},
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
            'Meta': {'ordering': "['id']", 'object_name': 'RawDataExtra'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['metricsmanager.RawDataCategory']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metric': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['metricsmanager.Metric']"})
        },
        'metricsmanager.rawdataextradata': {
            'Meta': {'ordering': "['row']", 'object_name': 'RawDataExtraData'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'raw_data_extra': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['metricsmanager.RawDataExtra']"}),
            'row': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['metricsmanager']