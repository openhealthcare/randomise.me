# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'TrialAnalysis.nobsa'
        db.add_column(u'trials_trialanalysis', 'nobsa',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'TrialAnalysis.nobsb'
        db.add_column(u'trials_trialanalysis', 'nobsb',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'TrialAnalysis.meana'
        db.add_column(u'trials_trialanalysis', 'meana',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'TrialAnalysis.meanb'
        db.add_column(u'trials_trialanalysis', 'meanb',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'TrialAnalysis.nobsa'
        db.delete_column(u'trials_trialanalysis', 'nobsa')

        # Deleting field 'TrialAnalysis.nobsb'
        db.delete_column(u'trials_trialanalysis', 'nobsb')

        # Deleting field 'TrialAnalysis.meana'
        db.delete_column(u'trials_trialanalysis', 'meana')

        # Deleting field 'TrialAnalysis.meanb'
        db.delete_column(u'trials_trialanalysis', 'meanb')


    models = {
        u'trials.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'trial': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trials.Trial']"})
        },
        u'trials.invitation': {
            'Meta': {'object_name': 'Invitation'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'trial': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trials.Trial']"})
        },
        u'trials.participant': {
            'Meta': {'object_name': 'Participant'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trials.Group']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'joined': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 6, 19, 0, 0)', 'blank': 'True'}),
            'trial': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trials.Trial']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['userprofiles.RMUser']", 'null': 'True', 'blank': 'True'})
        },
        u'trials.report': {
            'Meta': {'object_name': 'Report'},
            'binary': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trials.Group']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trials.Participant']", 'null': 'True', 'blank': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'trial': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trials.Trial']"}),
            'variable': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trials.Variable']"})
        },
        u'trials.trial': {
            'Meta': {'object_name': 'Trial'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 6, 19, 0, 0)'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'ending_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'ending_reports': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ending_style': ('django.db.models.fields.CharField', [], {'default': "'ma'", 'max_length': '2'}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'group_a': ('django.db.models.fields.TextField', [], {}),
            'group_a_expected': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'group_b': ('django.db.models.fields.TextField', [], {}),
            'group_b_impressed': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'instruction_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'instruction_delivery': ('django.db.models.fields.CharField', [], {'default': "'im'", 'max_length': '2'}),
            'instruction_hours_after': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'is_edited': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'min_participants': ('django.db.models.fields.IntegerField', [], {}),
            'n1trial': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['userprofiles.RMUser']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'child'", 'null': 'True', 'to': u"orm['trials.Trial']"}),
            'participants': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'recruitment': ('django.db.models.fields.CharField', [], {'default': "'an'", 'max_length': '2'}),
            'reporting_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'reporting_freq': ('django.db.models.fields.CharField', [], {'default': "'da'", 'max_length': '2'}),
            'reporting_style': ('django.db.models.fields.CharField', [], {'default': "'wh'", 'max_length': '2'}),
            'secret_info': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'stopped': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'trials.trialanalysis': {
            'Meta': {'object_name': 'TrialAnalysis'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mean': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'meana': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'meanb': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'nobsa': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nobsb': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'power_large': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'power_med': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'power_small': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'sd': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'trial': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trials.Trial']"})
        },
        u'trials.tutorialexample': {
            'Meta': {'object_name': 'TutorialExample'},
            'group_a': ('django.db.models.fields.TextField', [], {}),
            'group_b': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'measure_question': ('django.db.models.fields.TextField', [], {}),
            'measure_style': ('django.db.models.fields.CharField', [], {'default': "'sc'", 'max_length': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'trials.variable': {
            'Meta': {'object_name': 'Variable'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'question': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'style': ('django.db.models.fields.CharField', [], {'default': "'sc'", 'max_length': '2'}),
            'trial': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trials.Trial']"})
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

    complete_apps = ['trials']