# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Lecture.vimeo_id'
        db.add_column('conference_lecture', 'vimeo_id',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Lecture.vimeo_id'
        db.delete_column('conference_lecture', 'vimeo_id')


    models = {
        'conference.addressbook': {
            'Meta': {'object_name': 'AddressBook'},
            'fb': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'habr': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'know_design': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'know_research': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'know_testing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'moikrug': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'no_book': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'no_group': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'no_invite': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['conference.Result']"}),
            'site': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'twitter': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'vk': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'work_clientside': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'work_designer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'work_director': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'work_manager': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'work_pm': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'work_programmer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'work_sale': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'work_student': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'work_teacher': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'work_tester': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'work_writer': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'conference.category': {
            'Meta': {'object_name': 'Category'},
            'class_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'conference.contacts': {
            'Meta': {'object_name': 'Contacts'},
            'comment': ('django.db.models.fields.TextField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'site': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'})
        },
        'conference.lecture': {
            'Meta': {'object_name': 'Lecture'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['conference.Category']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'presentation': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'slideshare_link': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'speaker': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['conference.Speaker']", 'symmetrical': 'False'}),
            'thesises': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'timing': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'vimeo_id': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'conference.lecturerate': {
            'Meta': {'object_name': 'LectureRate'},
            'favorite': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lecture': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['conference.Lecture']"}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['conference.Result']"}),
            'theme_rate': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'total_rate': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'})
        },
        'conference.menu': {
            'Meta': {'object_name': 'Menu'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'weight': ('django.db.models.fields.IntegerField', [], {})
        },
        'conference.organization': {
            'Meta': {'object_name': 'Organization'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'facebook': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'site': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'conference.participant': {
            'Meta': {'unique_together': "(('first_name', 'last_name', 'email'),)", 'object_name': 'Participant'},
            'allow_news': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'company_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'confirmed': ('django.db.models.fields.CharField', [], {'default': "'u'", 'max_length': '3', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '24'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'})
        },
        'conference.participantfuture': {
            'Meta': {'unique_together': "(('first_name', 'last_name', 'email'),)", 'object_name': 'ParticipantFuture'},
            'company_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'})
        },
        'conference.partner': {
            'Meta': {'object_name': 'Partner'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['conference.Organization']"}),
            'partner_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['conference.PartnerStatus']"}),
            'weight': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'conference.partnerstatus': {
            'Meta': {'object_name': 'PartnerStatus'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'show_always': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title_plural': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'weight': ('django.db.models.fields.IntegerField', [], {})
        },
        'conference.person': {
            'Meta': {'object_name': 'Person'},
            'about': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '64', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['conference.Organization']", 'null': 'True', 'blank': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'site': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'twitter': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'})
        },
        'conference.result': {
            'Meta': {'object_name': 'Result'},
            'allow_partners': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'company_size': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'conf_rate_1': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'conf_rate_2': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'conf_rate_3': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'conf_rate_4': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['conference.Participant']", 'unique': 'True'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'position_custom': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'resume_1': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'resume_2': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'})
        },
        'conference.schedulesection': {
            'Meta': {'object_name': 'ScheduleSection'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['conference.Category']", 'null': 'True', 'blank': 'True'}),
            'duration': ('django.db.models.fields.IntegerField', [], {'default': '15'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lecture': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['conference.Lecture']", 'null': 'True', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.TimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'})
        },
        'conference.speaker': {
            'Meta': {'object_name': 'Speaker'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['conference.Person']"})
        }
    }

    complete_apps = ['conference']