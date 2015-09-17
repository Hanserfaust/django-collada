# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'FooBarScene.update_interval'
        db.add_column(u'django_collada_foobarscene', 'update_interval',
                      self.gf('django.db.models.fields.IntegerField')(default=1000),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'FooBarScene.update_interval'
        db.delete_column(u'django_collada_foobarscene', 'update_interval')


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
            'quick_collada': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'})
        },
        u'django_collada.foobar': {
            'Meta': {'object_name': 'FooBar'},
            'color': ('django.db.models.fields.CharField', [], {'default': "'ABCDEF'", 'max_length': '16'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'x_coord': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'y_coord': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'z_coord': ('django.db.models.fields.FloatField', [], {'default': '0.0'})
        },
        u'django_collada.foobarscene': {
            'Meta': {'ordering': "['-created', 'name']", 'object_name': 'FooBarScene', '_ormbases': [u'django_collada.ColladaScene']},
            u'colladascene_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['django_collada.ColladaScene']", 'unique': 'True', 'primary_key': 'True'}),
            'data_source_mappings': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['django_collada.SceneToDataSourceMapping']", 'symmetrical': 'False', 'blank': 'True'}),
            'update_interval': ('django.db.models.fields.IntegerField', [], {'default': '1000'})
        },
        u'django_collada.scenetodatasourcemapping': {
            'Meta': {'object_name': 'SceneToDataSourceMapping'},
            'foobar': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_collada.FooBar']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node_id': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        }
    }

    complete_apps = ['django_collada']