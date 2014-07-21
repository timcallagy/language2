# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table(u'lambada_userprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('payment_addr', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('skype_addr', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('timezone', self.gf('django.db.models.fields.CharField')(default='GMT', max_length=255)),
            ('language', self.gf('django.db.models.fields.CharField')(default='en', max_length=255)),
        ))
        db.send_create_signal(u'lambada', ['UserProfile'])

        # Adding model 'Subscription'
        db.create_table(u'lambada_subscription', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('userProfile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lambada.UserProfile'])),
        ))
        db.send_create_signal(u'lambada', ['Subscription'])

        # Adding model 'Rating'
        db.create_table(u'lambada_rating', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('userProfile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lambada.UserProfile'])),
        ))
        db.send_create_signal(u'lambada', ['Rating'])

        # Adding model 'Comment'
        db.create_table(u'lambada_comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('userProfile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lambada.UserProfile'])),
        ))
        db.send_create_signal(u'lambada', ['Comment'])

        # Adding model 'Topic'
        db.create_table(u'lambada_topic', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('headline', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('language', self.gf('django.db.models.fields.CharField')(default='en', max_length=255)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 7, 20, 0, 0))),
            ('learners_text', self.gf('tinymce.models.HTMLField')()),
            ('guides_text', self.gf('tinymce.models.HTMLField')()),
            ('published', self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True)),
        ))
        db.send_create_signal(u'lambada', ['Topic'])

        # Adding model 'TopicLikes'
        db.create_table(u'lambada_topiclikes', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('userProfile', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['lambada.UserProfile'])),
            ('topic', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['lambada.Topic'])),
        ))
        db.send_create_signal(u'lambada', ['TopicLikes'])

        # Adding unique constraint on 'TopicLikes', fields ['userProfile', 'topic']
        db.create_unique(u'lambada_topiclikes', ['userProfile_id', 'topic_id'])

        # Adding model 'Practice'
        db.create_table(u'lambada_practice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('topic', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lambada.Topic'])),
            ('dateTime', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'lambada', ['Practice'])

        # Adding model 'Report'
        db.create_table(u'lambada_report', (
            ('practice', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['lambada.Practice'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'lambada', ['Report'])

        # Adding model 'Recording'
        db.create_table(u'lambada_recording', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('report', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lambada.Report'])),
            ('blob', self.gf('django.db.models.fields.BinaryField')(blank=True)),
            ('partNum', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'lambada', ['Recording'])


    def backwards(self, orm):
        # Removing unique constraint on 'TopicLikes', fields ['userProfile', 'topic']
        db.delete_unique(u'lambada_topiclikes', ['userProfile_id', 'topic_id'])

        # Deleting model 'UserProfile'
        db.delete_table(u'lambada_userprofile')

        # Deleting model 'Subscription'
        db.delete_table(u'lambada_subscription')

        # Deleting model 'Rating'
        db.delete_table(u'lambada_rating')

        # Deleting model 'Comment'
        db.delete_table(u'lambada_comment')

        # Deleting model 'Topic'
        db.delete_table(u'lambada_topic')

        # Deleting model 'TopicLikes'
        db.delete_table(u'lambada_topiclikes')

        # Deleting model 'Practice'
        db.delete_table(u'lambada_practice')

        # Deleting model 'Report'
        db.delete_table(u'lambada_report')

        # Deleting model 'Recording'
        db.delete_table(u'lambada_recording')


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
        u'lambada.comment': {
            'Meta': {'object_name': 'Comment'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'userProfile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lambada.UserProfile']"})
        },
        u'lambada.practice': {
            'Meta': {'object_name': 'Practice'},
            'dateTime': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lambada.Topic']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'lambada.rating': {
            'Meta': {'object_name': 'Rating'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'userProfile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lambada.UserProfile']"})
        },
        u'lambada.recording': {
            'Meta': {'object_name': 'Recording'},
            'blob': ('django.db.models.fields.BinaryField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'partNum': ('django.db.models.fields.IntegerField', [], {}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lambada.Report']"})
        },
        u'lambada.report': {
            'Meta': {'object_name': 'Report'},
            'practice': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['lambada.Practice']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'lambada.subscription': {
            'Meta': {'object_name': 'Subscription'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'userProfile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lambada.UserProfile']"})
        },
        u'lambada.topic': {
            'Meta': {'object_name': 'Topic'},
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 7, 20, 0, 0)'}),
            'guides_text': ('tinymce.models.HTMLField', [], {}),
            'headline': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '255'}),
            'learners_text': ('tinymce.models.HTMLField', [], {}),
            'published': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'})
        },
        u'lambada.topiclikes': {
            'Meta': {'unique_together': "(('userProfile', 'topic'),)", 'object_name': 'TopicLikes'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['lambada.Topic']"}),
            'userProfile': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['lambada.UserProfile']"})
        },
        u'lambada.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '255'}),
            'payment_addr': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'skype_addr': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'timezone': ('django.db.models.fields.CharField', [], {'default': "'GMT'", 'max_length': '255'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['lambada']