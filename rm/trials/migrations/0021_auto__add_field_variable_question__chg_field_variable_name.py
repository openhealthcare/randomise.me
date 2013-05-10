# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Variable.question'
        db.add_column(u'trials_variable', 'question',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)


        # Changing field 'Variable.name'
        db.alter_column(u'trials_variable', 'name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

    def backwards(self, orm):
        # Deleting field 'Variable.question'
        db.delete_column(u'trials_variable', 'question')


        # User chose to not deal with backwards NULL issues for 'Variable.name'
        raise RuntimeError("Cannot reverse this migration. 'Variable.name' and its values cannot be restored.")

    models = {
        u'trials.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'trial': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trials.Trial']"})
        },
        u'trials.participant': {
            'Meta': {'object_name': 'Participant'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trials.Group']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'trial': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trials.Trial']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['userprofiles.RMUser']"})
        },
        u'trials.report': {
            'Meta': {'object_name': 'Report'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trials.Group']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'trial': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trials.Trial']"}),
            'variable': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trials.Variable']"})
        },
        u'trials.singleuserallocation': {
            'Meta': {'object_name': 'SingleUserAllocation'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'group': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'trial': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trials.SingleUserTrial']"})
        },
        u'trials.singleuserreport': {
            'Meta': {'object_name': 'SingleUserReport'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'group': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {}),
            'trial': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trials.SingleUserTrial']"})
        },
        u'trials.singleusertrial': {
            'Meta': {'object_name': 'SingleUserTrial'},
            'finish_date': ('django.db.models.fields.DateField', [], {}),
            'group_a': ('django.db.models.fields.TextField', [], {}),
            'group_b': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['userprofiles.RMUser']"}),
            'question': ('django.db.models.fields.TextField', [], {}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'variable': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'trials.trial': {
            'Meta': {'object_name': 'Trial'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'finish_date': ('django.db.models.fields.DateField', [], {}),
            'group_a': ('django.db.models.fields.TextField', [], {}),
            'group_a_expected': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'group_b': ('django.db.models.fields.TextField', [], {}),
            'group_b_impressed': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_participants': ('django.db.models.fields.IntegerField', [], {}),
            'min_participants': ('django.db.models.fields.IntegerField', [], {}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['userprofiles.RMUser']"}),
            'participants': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'recruiting': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'style': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        u'trials.variable': {
            'Meta': {'object_name': 'Variable'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'question': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'style': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'trial': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trials.Trial']"})
        },
        u'userprofiles.rmuser': {
            'Meta': {'object_name': 'RMUser'},
            'account': ('django.db.models.fields.CharField', [], {'default': "'st'", 'max_length': '2'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '254'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40', 'db_index': 'True'})
        }
    }

    complete_apps = ['trials']