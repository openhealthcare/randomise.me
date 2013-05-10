# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'RMUser.name'
        db.add_column(u'userprofiles_rmuser', 'name',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'RMUser.dob'
        db.add_column(u'userprofiles_rmuser', 'dob',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'RMUser.gender'
        db.add_column(u'userprofiles_rmuser', 'gender',
                      self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True),
                      keep_default=False)

        # Adding field 'RMUser.postcode'
        db.add_column(u'userprofiles_rmuser', 'postcode',
                      self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'RMUser.name'
        db.delete_column(u'userprofiles_rmuser', 'name')

        # Deleting field 'RMUser.dob'
        db.delete_column(u'userprofiles_rmuser', 'dob')

        # Deleting field 'RMUser.gender'
        db.delete_column(u'userprofiles_rmuser', 'gender')

        # Deleting field 'RMUser.postcode'
        db.delete_column(u'userprofiles_rmuser', 'postcode')


    models = {
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
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40', 'db_index': 'True'})
        }
    }

    complete_apps = ['userprofiles']