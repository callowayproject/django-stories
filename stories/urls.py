#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""URL definitions for news stories
"""
try:
    from django.conf.urls.defaults import patterns, url
except ImportError:
    from django.conf.urls import patterns, url
from django.views.generic import (ArchiveIndexView, YearArchiveView,
    MonthArchiveView, WeekArchiveView, DayArchiveView, TodayArchiveView,
    DateDetailView)
from models import Story

info_dict = {
    'queryset': Story.published.all(),
    'date_field': 'publish_date',
    'allow_empty': True
}

print_info_dict = dict(info_dict.items() + [('template_name', 'stories/story_print.html')])
print_info_dict.pop('allow_empty')

comment_info_dict = dict(info_dict.items() + [('template_name', 'stories/story_comments.html')])
comment_info_dict.pop('allow_empty')

urlpatterns = patterns('',

    # news archive index
    url(
        r'^$',
        ArchiveIndexView.as_view(**info_dict),
        name='news_archive_index'
    ),
    # news archive year list
    url(
        r'^(?P<year>\d{4})/$',
        YearArchiveView.as_view(**info_dict),
        name='news_archive_year'
    ),
    # news archive month list
    url(
        r'^(?P<year>\d{4})/(?P<month>\w{3})/$',
        MonthArchiveView.as_view(**info_dict),
        name='news_archive_month'
    ),
    # news archive week list
    url(
        r'^(?P<year>\d{4})/(?P<week>\d{1,2})/$',
        WeekArchiveView.as_view(**info_dict),
        name='news_archive_week'
    ),
    # news archive day list
    url(
        r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/$',
        DayArchiveView.as_view(**info_dict),
        name='news_archive_day'
    ),
    # news archive today list
    url(
        r'^today/$',
        TodayArchiveView.as_view(**info_dict),
        name='news_archive_day'
    ),
    # story detail
    url(
        r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$',
        'stories.views.pag_story_detail',
        name='news_detail'
    ),
    #story print detail
    url(
        r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/print/$',
        DateDetailView.as_view(**print_info_dict),
        name='news_detail_print',
    ),
    #story comments
    url(
        r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/comments/$',
        DateDetailView.as_view(**comment_info_dict),
        name='news_detail_comments',
    ),

)
