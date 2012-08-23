# -*- coding: utf-8 -*-
import datetime
from south.creator import freezer
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

from stories.models import Story
from stories.settings import AUTHOR_MODEL

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

        # Get the name and column name of the m2m author field
        field, a, b, c = Story._meta.get_field_by_name('authors')
        m2m_column_name = field.m2m_reverse_name()
        field_name = field.m2m_reverse_field_name()

        # Adding M2M table for field authors on 'Story'
        db.create_table('stories_story_authors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('story', models.ForeignKey(orm['stories.story'], null=False)),
            (field_name, models.ForeignKey(orm[AUTHOR_MODEL], null=False))
        ))
        db.create_unique('stories_story_authors', ['story_id', m2m_column_name])


    def backwards(self, orm):
        # Removing unique constraint on 'Story', fields ['publish_date', 'slug']
        db.delete_unique('stories_story', ['publish_date', 'slug'])

        # Deleting model 'Story'
        db.delete_table('stories_story')

        # Removing M2M table for field authors on 'Story'
        db.delete_table('stories_story_authors')


    models = freezer.freeze_apps(['stories'])

    complete_apps = ['stories']
