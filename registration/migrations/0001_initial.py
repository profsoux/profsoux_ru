# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Item'
        db.create_table('registration_item', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['conference.Event'])),
        ))
        db.send_create_signal('registration', ['Item'])

        # Adding model 'ItemPrice'
        db.create_table('registration_itemprice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registration.Item'])),
            ('value', self.gf('django.db.models.fields.IntegerField')()),
            ('available_from', self.gf('django.db.models.fields.DateField')()),
            ('available_to', self.gf('django.db.models.fields.DateField')()),
            ('is_cancelled', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('registration', ['ItemPrice'])


    def backwards(self, orm):
        # Deleting model 'Item'
        db.delete_table('registration_item')

        # Deleting model 'ItemPrice'
        db.delete_table('registration_itemprice')


    models = {
        'conference.event': {
            'Meta': {'object_name': 'Event'},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'coordinates': ('django.db.models.fields.CharField', [], {'max_length': '24', 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'place': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'place_note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'registration_end': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'registration_start': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'show_programm': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'use_flows': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'use_sections': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'registration.item': {
            'Meta': {'object_name': 'Item'},
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['conference.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'registration.itemprice': {
            'Meta': {'ordering': "['available_from']", 'object_name': 'ItemPrice'},
            'available_from': ('django.db.models.fields.DateField', [], {}),
            'available_to': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_cancelled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['registration.Item']"}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['registration']