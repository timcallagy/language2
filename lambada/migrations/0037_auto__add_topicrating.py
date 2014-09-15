# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TopicRating'
        db.create_table(u'lambada_topicrating', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('learner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('practice', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lambada.Practice'])),
            ('rating', self.gf('django.db.models.fields.IntegerField')(default='0')),
        ))
        db.send_create_signal(u'lambada', ['TopicRating'])


    def backwards(self, orm):
        # Deleting model 'TopicRating'
        db.delete_table(u'lambada_topicrating')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'lambada.channeldefault': {
            'Meta': {'object_name': 'ChannelDefault'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'practice_pk': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'lambada.channelprivate': {
            'Meta': {'object_name': 'ChannelPrivate'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'practice_pk': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'lambada.coachrating': {
            'Meta': {'object_name': 'CoachRating'},
            'coach': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lambada.UserProfile']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'practice': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lambada.Practice']"}),
            'rating': ('django.db.models.fields.IntegerField', [], {'default': "'0'"})
        },
        u'lambada.comment': {
            'Meta': {'object_name': 'Comment'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'userProfile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lambada.UserProfile']"})
        },
        u'lambada.learnerrecording': {
            'Meta': {'object_name': 'LearnerRecording'},
            'call_start_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'practice': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lambada.Practice']"}),
            'recording': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'lambada.practice': {
            'Meta': {'object_name': 'Practice'},
            'callTimeElapsed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'coach': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'coach_recording_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'dateTime': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'learner_recording_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'learners_writing': ('tinymce.models.HTMLField', [], {'max_length': '255'}),
            'rating': ('django.db.models.fields.IntegerField', [], {'default': "'0'"}),
            'speaking_report_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'timeUntil': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lambada.Topic']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'writing_complete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'writing_report_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'lambada.rating': {
            'Meta': {'object_name': 'Rating'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'userProfile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lambada.UserProfile']"})
        },
        u'lambada.speakingerror': {
            'Meta': {'object_name': 'SpeakingError'},
            'coach': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'correction_recording': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'correction_recording_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'correction_text': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'error_time_min': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'error_time_sec': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'learner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'learnerRecording': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lambada.LearnerRecording']"}),
            'practice': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lambada.Practice']"})
        },
        u'lambada.subscription': {
            'Meta': {'object_name': 'Subscription'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'userProfile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lambada.UserProfile']"})
        },
        u'lambada.topic': {
            'Meta': {'object_name': 'Topic'},
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 15, 0, 0)'}),
            'guides_speaking_instructions': ('tinymce.models.HTMLField', [], {}),
            'headline': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '255'}),
            'learners_speaking_instructions': ('tinymce.models.HTMLField', [], {}),
            'learners_writing_instructions': ('tinymce.models.HTMLField', [], {}),
            'published': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'})
        },
        u'lambada.topicrating': {
            'Meta': {'object_name': 'TopicRating'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'learner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'practice': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lambada.Practice']"}),
            'rating': ('django.db.models.fields.IntegerField', [], {'default': "'0'"})
        },
        u'lambada.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '255'}),
            'payment_addr': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'timezone': ('django.db.models.fields.CharField', [], {'default': "'GMT'", 'max_length': '255'}),
            'total_coach_rating': ('django.db.models.fields.IntegerField', [], {'default': "'0'"}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'lambada.writingerror': {
            'Meta': {'object_name': 'WritingError'},
            'coach': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'correction_text': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'learner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'original_text': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'practice': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lambada.Practice']"})
        }
    }

    complete_apps = ['lambada']