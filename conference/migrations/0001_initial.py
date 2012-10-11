# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Menu'
        db.create_table('conference_menu', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('link', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('weight', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('conference', ['Menu'])

        # Adding model 'Person'
        db.create_table('conference_person', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('about', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=64, blank=True)),
            ('twitter', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('site', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['conference.Organization'], null=True, blank=True)),
        ))
        db.send_create_signal('conference', ['Person'])

        # Adding model 'Organization'
        db.create_table('conference_organization', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('site', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('facebook', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('conference', ['Organization'])

        # Adding model 'Partner'
        db.create_table('conference_partner', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['conference.Organization'])),
            ('partner_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['conference.PartnerStatus'])),
            ('weight', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('conference', ['Partner'])

        # Adding model 'PartnerStatus'
        db.create_table('conference_partnerstatus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('title_plural', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('weight', self.gf('django.db.models.fields.IntegerField')()),
            ('show_always', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('conference', ['PartnerStatus'])

        # Adding model 'Lecture'
        db.create_table('conference_lecture', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['conference.Category'])),
            ('timing', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('thesises', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('presentation', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('slideshare_link', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('conference', ['Lecture'])

        # Adding M2M table for field speaker on 'Lecture'
        db.create_table('conference_lecture_speaker', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('lecture', models.ForeignKey(orm['conference.lecture'], null=False)),
            ('speaker', models.ForeignKey(orm['conference.speaker'], null=False))
        ))
        db.create_unique('conference_lecture_speaker', ['lecture_id', 'speaker_id'])

        # Adding model 'Speaker'
        db.create_table('conference_speaker', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['conference.Person'])),
        ))
        db.send_create_signal('conference', ['Speaker'])

        # Adding model 'Category'
        db.create_table('conference_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('class_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('conference', ['Category'])

        # Adding model 'ScheduleSection'
        db.create_table('conference_schedulesection', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start_time', self.gf('django.db.models.fields.TimeField')()),
            ('duration', self.gf('django.db.models.fields.IntegerField')(default=15)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['conference.Category'], null=True, blank=True)),
            ('lecture', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['conference.Lecture'], null=True, blank=True)),
        ))
        db.send_create_signal('conference', ['ScheduleSection'])

        # Adding model 'Participant'
        db.create_table('conference_participant', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=24)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('company_name', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('position', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('allow_news', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('confirmed', self.gf('django.db.models.fields.CharField')(default='u', max_length=3, blank=True)),
        ))
        db.send_create_signal('conference', ['Participant'])

        # Adding unique constraint on 'Participant', fields ['first_name', 'last_name', 'email']
        db.create_unique('conference_participant', ['first_name', 'last_name', 'email'])

        # Adding model 'ParticipantFuture'
        db.create_table('conference_participantfuture', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('company_name', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('position', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
        ))
        db.send_create_signal('conference', ['ParticipantFuture'])

        # Adding unique constraint on 'ParticipantFuture', fields ['first_name', 'last_name', 'email']
        db.create_unique('conference_participantfuture', ['first_name', 'last_name', 'email'])

        # Adding model 'Contacts'
        db.create_table('conference_contacts', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('site', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('conference', ['Contacts'])

        # Adding model 'Result'
        db.create_table('conference_result', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('participant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['conference.Participant'], unique=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('company_size', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('position', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('position_custom', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('site', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('conf_rate_1', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('conf_rate_2', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('conf_rate_3', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('conf_rate_4', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('resume_1', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('resume_2', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('allow_partners', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('conference', ['Result'])

        # Adding model 'AddressBook'
        db.create_table('conference_addressbook', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('participant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['conference.Result'])),
            ('moikrug', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('twitter', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('fb', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('vk', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('habr', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('site', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('know_design', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('know_research', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('know_testing', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('work_pm', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('work_programmer', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('work_clientside', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('work_manager', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('work_director', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('work_sale', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('work_tester', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('work_teacher', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('work_writer', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('work_student', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('work_designer', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('no_book', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('no_group', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('no_invite', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('conference', ['AddressBook'])

        # Adding model 'LectureRate'
        db.create_table('conference_lecturerate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('participant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['conference.Result'])),
            ('lecture', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['conference.Lecture'])),
            ('theme_rate', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('total_rate', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('favorite', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('conference', ['LectureRate'])


    def backwards(self, orm):
        # Removing unique constraint on 'ParticipantFuture', fields ['first_name', 'last_name', 'email']
        db.delete_unique('conference_participantfuture', ['first_name', 'last_name', 'email'])

        # Removing unique constraint on 'Participant', fields ['first_name', 'last_name', 'email']
        db.delete_unique('conference_participant', ['first_name', 'last_name', 'email'])

        # Deleting model 'Menu'
        db.delete_table('conference_menu')

        # Deleting model 'Person'
        db.delete_table('conference_person')

        # Deleting model 'Organization'
        db.delete_table('conference_organization')

        # Deleting model 'Partner'
        db.delete_table('conference_partner')

        # Deleting model 'PartnerStatus'
        db.delete_table('conference_partnerstatus')

        # Deleting model 'Lecture'
        db.delete_table('conference_lecture')

        # Removing M2M table for field speaker on 'Lecture'
        db.delete_table('conference_lecture_speaker')

        # Deleting model 'Speaker'
        db.delete_table('conference_speaker')

        # Deleting model 'Category'
        db.delete_table('conference_category')

        # Deleting model 'ScheduleSection'
        db.delete_table('conference_schedulesection')

        # Deleting model 'Participant'
        db.delete_table('conference_participant')

        # Deleting model 'ParticipantFuture'
        db.delete_table('conference_participantfuture')

        # Deleting model 'Contacts'
        db.delete_table('conference_contacts')

        # Deleting model 'Result'
        db.delete_table('conference_result')

        # Deleting model 'AddressBook'
        db.delete_table('conference_addressbook')

        # Deleting model 'LectureRate'
        db.delete_table('conference_lecturerate')


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
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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