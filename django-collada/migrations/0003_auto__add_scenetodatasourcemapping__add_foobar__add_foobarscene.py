# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SceneToDataSourceMapping'
        db.create_table(u'django_collada_scenetodatasourcemapping', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('node_id', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('foobar', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_collada.FooBar'])),
        ))
        db.send_create_signal(u'django_collada', ['SceneToDataSourceMapping'])

        # Adding model 'FooBar'
        db.create_table(u'django_collada_foobar', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('x_coord', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('y_coord', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('z_coord', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('color', self.gf('django.db.models.fields.CharField')(default='ABCDEF', max_length=16)),
        ))
        db.send_create_signal(u'django_collada', ['FooBar'])

        # Adding model 'FooBarScene'
        db.create_table(u'django_collada_foobarscene', (
            (u'colladascene_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['django_collada.ColladaScene'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'django_collada', ['FooBarScene'])

        # Adding M2M table for field data_source_mappings on 'FooBarScene'
        db.create_table(u'django_collada_foobarscene_data_source_mappings', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('foobarscene', models.ForeignKey(orm[u'django_collada.foobarscene'], null=False)),
            ('scenetodatasourcemapping', models.ForeignKey(orm[u'django_collada.scenetodatasourcemapping'], null=False))
        ))
        db.create_unique(u'django_collada_foobarscene_data_source_mappings', ['foobarscene_id', 'scenetodatasourcemapping_id'])


    def backwards(self, orm):
        # Deleting model 'SceneToDataSourceMapping'
        db.delete_table(u'django_collada_scenetodatasourcemapping')

        # Deleting model 'FooBar'
        db.delete_table(u'django_collada_foobar')

        # Deleting model 'FooBarScene'
        db.delete_table(u'django_collada_foobarscene')

        # Removing M2M table for field data_source_mappings on 'FooBarScene'
        db.delete_table('django_collada_foobarscene_data_source_mappings')


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
            'data_source_mappings': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['django_collada.SceneToDataSourceMapping']", 'symmetrical': 'False'})
        },
        u'django_collada.scenetodatasourcemapping': {
            'Meta': {'object_name': 'SceneToDataSourceMapping'},
            'foobar': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_collada.FooBar']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node_id': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        }
    }

    complete_apps = ['django_collada']