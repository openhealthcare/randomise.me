# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Vote', fields ['voter', 'contenttype', 'object_id']
        db.delete_unique(u'suffrage_vote', ['voter_id', 'contenttype_id', 'object_id'])

        # Deleting field 'Vote.contenttype'
        db.delete_column(u'suffrage_vote', 'contenttype_id')

        # Adding field 'Vote.content_type'
        db.add_column(u'suffrage_vote', 'content_type',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=27, to=orm['contenttypes.ContentType']),
                      keep_default=False)

        # Adding unique constraint on 'Vote', fields ['voter', 'object_id', 'content_type']
#        db.create_unique(u'suffrage_vote', ['voter_id', 'object_id', 'content_type_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Vote', fields ['voter', 'object_id', 'content_type']
        db.delete_unique(u'suffrage_vote', ['voter_id', 'object_id', 'content_type_id'])


        # User chose to not deal with backwards NULL issues for 'Vote.contenttype'
        raise RuntimeError("Cannot reverse this migration. 'Vote.contenttype' and its values cannot be restored.")
        # Deleting field 'Vote.content_type'
        db.delete_column(u'suffrage_vote', 'content_type_id')

        # Adding unique constraint on 'Vote', fields ['voter', 'contenttype', 'object_id']
        db.create_unique(u'suffrage_vote', ['voter_id', 'contenttype_id', 'object_id'])


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'suffrage.vote': {
            'Meta': {'unique_together': "(('voter', 'content_type', 'object_id'),)", 'object_name': 'Vote'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {}),
            'val': ('django.db.models.fields.SmallIntegerField', [], {}),
            'voter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['userprofiles.RMUser']"})
        },
        u'userprofiles.rmuser': {
            'Meta': {'object_name': 'RMUser'},
            'account': ('django.db.models.fields.CharField', [], {'default': "'st'", 'max_length': '2'}),
            'dob': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '254'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'receive_emails': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'receive_questions': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'single_page': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40', 'db_index': 'True'})
        }
    }

    complete_apps = ['suffrage']
