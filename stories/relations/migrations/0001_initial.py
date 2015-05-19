# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0001_initial'),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoryRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('relation_type', models.CharField(help_text="A generic text field to tag a relation, such as 'leadphoto'.", max_length=b'200', null=True, verbose_name='Relation Type', blank=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('story', models.ForeignKey(to='stories.Story')),
            ],
            options={
                'db_table': 'stories_storyrelation',
            },
            bases=(models.Model,),
        ),
    ]
