# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UnitCategory'
        db.create_table(u'metrics_manager_unitcategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
        ))
        db.send_create_signal(u'metrics_manager', ['UnitCategory'])

        # Adding model 'Unit'
        db.create_table(u'metrics_manager_unit', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('unit_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['metrics_manager.UnitCategory'])),
        ))
        db.send_create_signal(u'metrics_manager', ['Unit'])

        # Adding model 'MetricInDomain'
        db.create_table(u'metrics_manager_metricindomain', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('domain_id', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'metrics_manager', ['MetricInDomain'])

        # Adding model 'Metric'
        db.create_table(u'metrics_manager_metric', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('acronym', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('keywords', self.gf('django.db.models.fields.CharField')(max_length=400)),
            ('geo_location', self.gf('django.db.models.fields.CharField')(max_length=1000, blank=True)),
            ('publisher', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('details_url', self.gf('django.db.models.fields.URLField')(max_length=500, blank=True)),
            ('license', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('user_id', self.gf('django.db.models.fields.IntegerField')()),
            ('language_id', self.gf('django.db.models.fields.IntegerField')()),
            ('ext_resource_id', self.gf('django.db.models.fields.IntegerField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('version', self.gf('django.db.models.fields.IntegerField')()),
            ('formula', self.gf('django.db.models.fields.CharField')(default='1', max_length=10000)),
            ('issued', self.gf('django.db.models.fields.DateTimeField')()),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['metrics_manager.Unit'])),
        ))
        db.send_create_signal(u'metrics_manager', ['Metric'])

        # Adding M2M table for field policy_domains on 'Metric'
        m2m_table_name = db.shorten_name(u'metrics_manager_metric_policy_domains')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('metric', models.ForeignKey(orm[u'metrics_manager.metric'], null=False)),
            ('metricindomain', models.ForeignKey(orm[u'metrics_manager.metricindomain'], null=False))
        ))
        db.create_unique(m2m_table_name, ['metric_id', 'metricindomain_id'])

        # Adding model 'RawData'
        db.create_table(u'metrics_manager_rawdata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('metric', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['metrics_manager.Metric'])),
            ('value', self.gf('django.db.models.fields.FloatField')()),
            ('from_date', self.gf('django.db.models.fields.DateField')()),
            ('to_date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'metrics_manager', ['RawData'])

        # Adding model 'RawDataCategory'
        db.create_table(u'metrics_manager_rawdatacategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'metrics_manager', ['RawDataCategory'])

        # Adding model 'RawDataExtra'
        db.create_table(u'metrics_manager_rawdataextra', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('raw_data', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['metrics_manager.RawData'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['metrics_manager.RawDataCategory'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'metrics_manager', ['RawDataExtra'])


    def backwards(self, orm):
        # Deleting model 'UnitCategory'
        db.delete_table(u'metrics_manager_unitcategory')

        # Deleting model 'Unit'
        db.delete_table(u'metrics_manager_unit')

        # Deleting model 'MetricInDomain'
        db.delete_table(u'metrics_manager_metricindomain')

        # Deleting model 'Metric'
        db.delete_table(u'metrics_manager_metric')

        # Removing M2M table for field policy_domains on 'Metric'
        db.delete_table(db.shorten_name(u'metrics_manager_metric_policy_domains'))

        # Deleting model 'RawData'
        db.delete_table(u'metrics_manager_rawdata')

        # Deleting model 'RawDataCategory'
        db.delete_table(u'metrics_manager_rawdatacategory')

        # Deleting model 'RawDataExtra'
        db.delete_table(u'metrics_manager_rawdataextra')


    models = {
        u'metrics_manager.metric': {
            'Meta': {'object_name': 'Metric'},
            'acronym': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'details_url': ('django.db.models.fields.URLField', [], {'max_length': '500', 'blank': 'True'}),
            'ext_resource_id': ('django.db.models.fields.IntegerField', [], {}),
            'formula': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '10000'}),
            'geo_location': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issued': ('django.db.models.fields.DateTimeField', [], {}),
            'keywords': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'language_id': ('django.db.models.fields.IntegerField', [], {}),
            'license': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'policy_domains': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['metrics_manager.MetricInDomain']", 'symmetrical': 'False'}),
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
            'raw_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['metrics_manager.RawData']"}),
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