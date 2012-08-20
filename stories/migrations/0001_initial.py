# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Story'
        db.create_table('stories_story', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('headline', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('tease_headline', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True)),
            ('subhead', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('non_staff_author', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('publish_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('publish_time', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('update_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('comments', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('comment_status', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('teaser', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('kicker', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('origin', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
        ))
        db.send_create_signal('stories', ['Story'])

        # Adding unique constraint on 'Story', fields ['publish_date', 'slug']
        db.create_unique('stories_story', ['publish_date', 'slug'])

        # Adding M2M table for field authors on 'Story'
        db.create_table('stories_story_authors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('story', models.ForeignKey(orm['stories.story'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('stories_story_authors', ['story_id', 'user_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Story', fields ['publish_date', 'slug']
        db.delete_unique('stories_story', ['publish_date', 'slug'])

        # Deleting model 'Story'
        db.delete_table('stories_story')

        # Removing M2M table for field authors on 'Story'
        db.delete_table('stories_story_authors')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'stories.story': {
            'Meta': {'ordering': "['-publish_date']", 'unique_together': "(('publish_date', 'slug'),)", 'object_name': 'Story'},
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'comment_status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'comments': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'headline': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kicker': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'non_staff_author': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'origin': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'publish_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'publish_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'subhead': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'tease_headline': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'teaser': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'update_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['stories']