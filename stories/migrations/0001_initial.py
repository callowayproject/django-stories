# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from stories.settings import AUTHOR_MODEL


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        migrations.swappable_dependency(AUTHOR_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('headline', models.CharField(max_length=100, verbose_name='Headline')),
                ('tease_headline', models.CharField(default=b'', max_length=100, verbose_name='Tease Headline', blank=True)),
                ('subhead', models.CharField(max_length=200, null=True, verbose_name='Subheadline', blank=True)),
                ('slug', models.SlugField(verbose_name='Slug')),
                ('non_staff_author', models.CharField(help_text='An HTML-formatted rendering of an author(s) not on staff.', max_length=200, null=True, verbose_name='Non-staff author(s)', blank=True)),
                ('publish_date', models.DateField(help_text='The date the original story was published', null=True, verbose_name='Publish Date', blank=True)),
                ('publish_time', models.TimeField(help_text='The time the original story was published', null=True, verbose_name='Publish Time', blank=True)),
                ('update_date', models.DateTimeField(help_text='The update date/time to display to the user', null=True, verbose_name='Update Date', blank=True)),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='Date Modified')),
                ('comments', models.BooleanField(default=True, verbose_name='Enable Comments?')),
                ('comment_status', models.IntegerField(default=1, verbose_name='Comment Status', choices=[(0, 'Comments Disabled'), (1, 'Comments Enabled'), (2, 'Comments Frozen')])),
                ('status', models.IntegerField(default=1, verbose_name='Published Status', choices=[(1, 'DRAFT'), (2, 'READY FOR EDITING'), (3, 'READY TO PUBLISH'), (4, 'PUBLISHED'), (5, 'REJECTED'), (6, 'UN-PUBLISHED')])),
                ('teaser', models.TextField(verbose_name='Teaser Text', blank=True)),
                ('kicker', models.CharField(max_length=50, null=True, verbose_name='Kicker', blank=True)),
                ('body', models.TextField(verbose_name='Body')),
                ('origin', models.IntegerField(default=0, verbose_name='Origin', choices=[(0, 'Admin')])),
                ('authors', models.ManyToManyField(to=AUTHOR_MODEL, null=True, verbose_name='Authors', blank=True)),
                ('site', models.ForeignKey(verbose_name='Site', to='sites.Site')),
            ],
            options={
                'ordering': ['-publish_date'],
                'get_latest_by': 'publish_date',
                'verbose_name': 'Story',
                'verbose_name_plural': 'Stories',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='story',
            unique_together=set([('publish_date', 'slug')]),
        ),
    ]
