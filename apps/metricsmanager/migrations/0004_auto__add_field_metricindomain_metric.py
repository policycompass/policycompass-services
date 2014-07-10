# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'MetricInDomain.metric'
        db.add_column(u'metrics_manager_metricindomain', 'metric',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['metrics_manager.Metric']),
                      keep_default=False)

        # Removing M2M table for field policy_domains on 'Metric'
        db.delete_table(db.shorten_name(u'metrics_manager_metric_policy_domains'))


    def backwards(self, orm):
        # Deleting field 'MetricInDomain.metric'
        db.delete_column(u'metrics_manager_metricindomain', 'metric_id')

        # Adding M2M table for field policy_domains on 'Metric'
        m2m_table_name = db.shorten_name(u'metrics_manager_metric_policy_domains')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('metric', models.ForeignKey(orm[u'metrics_manager.metric'], null=False)),
            ('metricindomain', models.ForeignKey(orm[u'metrics_manager.metricindomain'], null=False))
        ))
        db.create_unique(m2m_table_name, ['metric_id', 'metricindomain_id'])


    models = {
        u'metrics_manager.metric': {
            'Meta': {'object_name': 'Metric'},
            'acronym': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'details_url': ('django.db.models.fields.URLField', [], {'max_length': '500', 'blank': 'True'}),
            'ext_resource_id': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'formula': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '10000'}),
            'geo_location': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issued': ('django.db.models.fields.DateField', [], {}),
            'keywords': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'language_id': ('django.db.models.fields.IntegerField', [], {}),
            'license': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'publisher': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['metrics_manager.Unit']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user_id': ('django.db.models.fields.IntegerField', [], {}),
            'version': ('django.db.models.fields.IntegerField', [], {})
        },
        u'metrics_manager.metricindomain': {
            'Meta': {'object_name': 'MetricInDomain'},
            'domain_id': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metric': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['metrics_manager.Metric']"})
        },
        u'metrics_manager.rawdata': {
            'Meta': {'object_name': 'RawData'},
            'from_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metric': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['metrics_manager.Metric']"}),
            'to_date': ('django.db.models.fields.DateField', [], {}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        u'metrics_manager.rawdatacategory': {
            'Meta': {'object_name': 'RawDataCategory'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'metrics_manager.rawdataextra': {
            'Meta': {'object_name': 'RawDataExtra'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['metrics_manager.RawDataCategory']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'raw_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['metrics_manager.RawData']"})
        },
        u'metrics_manager.rawdataextradata': {
            'Meta': {'object_name': 'RawDataExtraData'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'raw_data_extra': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['metrics_manager.RawDataExtra']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'metrics_manager.unit': {
            'Meta': {'object_name': 'Unit'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'unit_category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['metrics_manager.UnitCategory']"})
        },
        u'metrics_manager.unitcategory': {
            'Meta': {'object_name': 'UnitCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        }
    }

    complete_apps = ['metrics_manager']