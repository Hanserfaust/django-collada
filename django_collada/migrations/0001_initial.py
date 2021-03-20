# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ColladaScene'
        db.create_table(u'django_collada_colladascene', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('filesystem_path', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('dae_file', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('file_type', self.gf('django.db.models.fields.CharField')(default='zip', max_length=16, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'django_collada', ['ColladaScene'])


    def backwards(self, orm):
        # Deleting model 'ColladaScene'
        db.delete_table(u'django_collada_colladascene')


    models = {
        u'django_collada.colladascene': {
            'Meta': {'ordering': "['-created', 'name']", 'object_name': 'ColladaScene'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dae_file': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'file_type': ('django.db.models.fields.CharField', [], {'default': "'zip'", 'max_length': '16', 'blank': 'True'}),
            'filesystem_path': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'})
        }
    }

    complete_apps = ['django_collada']