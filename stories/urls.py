# -*- coding: utf-8 -*-
"""URL definitions for news stories
"""

from django.conf.urls.defaults import *
from models import Story

info_dict = {
    'queryset': Story.published.all(),
    'template_object_name': 'story',
    'date_field': 'publish_date',
    'allow_empty': True
}

print_info_dict = dict(info_dict.items() + [('template_name','stories/story_print.html')])
print_info_dict.pop('allow_empty')

comment_info_dict = dict(info_dict.items() + [('template_name','stories/story_comments.html')])
comment_info_dict.pop('allow_empty')

urlpatterns = patterns('',
                      
    # news archive index
    url(
        regex  = '^$',
        view   = 'django.views.generic.date_based.archive_index',
        kwargs = info_dict,
        name   = 'news_archive_index'
    ),
    # news archive year list
    url(
        regex  = '^(?P<year>\d{4})/$',
        view   = 'django.views.generic.date_based.archive_year',
        kwargs = info_dict,
        name   = 'news_archive_year'
    ),
    # news archive month list
    url(
        regex  = '^(?P<year>\d{4})/(?P<month>\w{3})/$',
        view   = 'django.views.generic.date_based.archive_month',
        kwargs = info_dict,
        name   = 'news_archive_month'
    ),
    # news archive week list
    url(
        regex  = '^(?P<year>\d{4})/(?P<week>\d{1,2})/$',
        view   = 'django.views.generic.date_based.archive_week',
        kwargs = info_dict,
        name   = 'news_archive_week'
    ),
    # news archive day list
    url(
        regex  = '^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/$',
        view   = 'django.views.generic.date_based.archive_day',
        kwargs = info_dict,
        name   = 'news_archive_day'
    ),
    # news archive today list
    url(
        regex  = '^today/$',
        view   = 'django.views.generic.date_based.archive_today',
        kwargs = info_dict,
        name   = 'news_archive_day'
    ),
    # story detail
    url(
        regex  = '^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$',
        view   = 'stories.views.pag_story_detail',
        name   = 'news_detail'
    ),
    #story print detail
    url(
        regex  = '^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/print/$',
        view   = 'django.views.generic.date_based.object_detail',
        kwargs = print_info_dict,
        name   = 'news_detail_print',
    ),
    #story comments
    url(
        regex  = '^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/comments/$',
        view   = 'django.views.generic.date_based.object_detail',
        kwargs = comment_info_dict,
        name   = 'news_detail_comments',
    ),
    
)
