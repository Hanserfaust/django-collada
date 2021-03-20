# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ColladaScene.quick_collada'
        db.add_column(u'django_collada_colladascene', 'quick_collada',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ColladaScene.quick_collada'
        db.delete_column(u'django_collada_colladascene', 'quick_collada')


    models = {
        u'django_collada.colladascene': {
            'Meta': {'ordering': "['-created', 'name']", 'object_name': 'ColladaScene'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dae_file': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'file_type': ('django.db.models.fields.CharField', [], {'default': "'zip'", 'max_length': '16', 'blank': 'True'}),
            'filesystem_path': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'quick_collada': ('django.db.models.fields.TextField', [], {'default': "''"})
        }
    }

    complete_apps = ['django_collada']