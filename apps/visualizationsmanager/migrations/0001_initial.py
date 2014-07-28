# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Visualization'
        db.create_table(u'visualizations_manager_visualization', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('keywords', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),            
            ('description', self.gf('django.db.models.fields.TextField')()),  
            ('user_id', self.gf('django.db.models.fields.IntegerField')()),                      
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('publisher', self.gf('django.db.models.fields.CharField')(blank=True, max_length=200)),   
            ('views_count', self.gf('django.db.models.fields.IntegerField')(default=0)),            
            ('visualization_type_id', self.gf('django.db.models.fields.IntegerField')()),
            ('language_id', self.gf('django.db.models.fields.IntegerField')()),
            ('status_flag_id', self.gf('django.db.models.fields.IntegerField')()), 
        ))
        db.send_create_signal(u'visualizations_manager', ['Visualization'])


    def backwards(self, orm):

        # Deleting model 'Visualization'
        db.delete_table(u'visualizations_manager_visualization')


    models = {
        u'visualizations_manager.visualization': {
            'Meta': {'object_name': 'Visualization'},            
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'user_id': ('django.db.models.fields.IntegerField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'publisher': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '200'}),
            'views_count': ('django.db.models.fields.IntegerField', [], {}),            
            'visualization_type_id': ('django.db.models.fields.IntegerField', [], {}),
            'language_id': ('django.db.models.fields.IntegerField', [], {}),
            'status_flag_id': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['visualizations_manager']