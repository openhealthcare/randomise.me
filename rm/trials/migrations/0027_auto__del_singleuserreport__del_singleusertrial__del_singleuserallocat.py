# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'SingleUserReport'
        db.delete_table(u'trials_singleuserreport')

        # Deleting model 'SingleUserTrial'
        db.delete_table(u'trials_singleusertrial')

        # Deleting model 'SingleUserAllocation'
        db.delete_table(u'trials_singleuserallocation')

        # Adding field 'Report.participant'
        db.add_column(u'trials_report', 'participant',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trials.Participant'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'SingleUserReport'
        db.create_table(u'trials_singleuserreport', (
            ('group', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('trial', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trials.SingleUserTrial'])),
            ('score', self.gf('django.db.models.fields.IntegerField')()),
            ('date', self.gf('django.db.models.fields.DateField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'trials', ['SingleUserReport'])

        # Adding model 'SingleUserTrial'
        db.create_table(u'trials_singleusertrial', (
            ('group_b', self.gf('django.db.models.fields.TextField')()),
            ('group_a', self.gf('django.db.models.fields.TextField')()),
            ('variable', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('finish_date', self.gf('django.db.models.fields.DateField')()),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['userprofiles.RMUser'])),
            ('question', self.gf('django.db.models.fields.TextField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'trials', ['SingleUserTrial'])

        # Adding model 'SingleUserAllocation'
        db.create_table(u'trials_singleuserallocation', (
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('trial', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trials.SingleUserTrial'])),
            ('group', self.gf('django.db.models.fields.CharField')(max_length=1)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'trials', ['SingleUserAllocation'])

        # Deleting field 'Report.participant'
        db.delete_column(u'trials_report', 'participant_id')


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
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['userprofiles.RMUser']", 'null': 'True', 'blank': 'True'})
        },
        u'trials.report': {
            'Meta': {'object_name': 'Report'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trials.Group']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trials.Participant']", 'null': 'True', 'blank': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'trial': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trials.Trial']"}),
            'variable': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trials.Variable']"})
        },
        u'trials.trial': {
            'Meta': {'object_name': 'Trial'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'finish_date': ('django.db.models.fields.DateField', [], {}),
            'group_a': ('django.db.models.fields.TextField', [], {}),
            'group_a_desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'group_a_expected': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'group_b': ('django.db.models.fields.TextField', [], {}),
            'group_b_desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'group_b_impressed': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_participants': ('django.db.models.fields.IntegerField', [], {}),
            'min_participants': ('django.db.models.fields.IntegerField', [], {}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['userprofiles.RMUser']"}),
            'participants': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'recruiting': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'recruitment': ('django.db.models.fields.CharField', [], {'default': "'an'", 'max_length': '2'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
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

    complete_apps = ['trials']