# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Trial'
        db.create_table(u'trials_trial', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('url', self.gf('django.db.models.fields.CharField')(unique=True, max_length=120)),
            ('question', self.gf('django.db.models.fields.TextField')()),
            ('style', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('group_a', self.gf('django.db.models.fields.TextField')()),
            ('group_b', self.gf('django.db.models.fields.TextField')()),
            ('instruct_style', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('instruct_hour', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('instruct_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('min_participants', self.gf('django.db.models.fields.IntegerField')()),
            ('max_participants', self.gf('django.db.models.fields.IntegerField')()),
            ('group_a_expected', self.gf('django.db.models.fields.IntegerField')()),
            ('group_b_impressed', self.gf('django.db.models.fields.IntegerField')()),
            ('finish_date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'trials', ['Trial'])


    def backwards(self, orm):
        # Deleting model 'Trial'
        db.delete_table(u'trials_trial')


    models = {
        u'trials.trial': {
            'Meta': {'object_name': 'Trial'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'finish_date': ('django.db.models.fields.DateField', [], {}),
            'group_a': ('django.db.models.fields.TextField', [], {}),
            'group_a_expected': ('django.db.models.fields.IntegerField', [], {}),
            'group_b': ('django.db.models.fields.TextField', [], {}),
            'group_b_impressed': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instruct_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'instruct_hour': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'instruct_style': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'max_participants': ('django.db.models.fields.IntegerField', [], {}),
            'min_participants': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'question': ('django.db.models.fields.TextField', [], {}),
            'style': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '120'})
        }
    }

    complete_apps = ['trials']