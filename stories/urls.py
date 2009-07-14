# -*- coding: utf-8 -*-
"""URL definitions for news stories
"""

from django.conf.urls.defaults import *
from models import Story

info_dict = {
    'queryset': Story.published_on_site.all(),
    'template_object_name': 'story',
    'date_field': 'publish_date'
}

urlpatterns = patterns('',
                      
    # news archive index
    url(
        regex  = '^$',
        view   = 'django.views.generic.date_based.archive_index',
        kwargs = info_dict,
        name   = 'news-archive_index'
    ),
    # news archive year list
    url(
        regex  = '^(?P<year>\d{4})/$',
        view   = 'django.views.generic.date_based.archive_year',
        kwargs = info_dict,
        name   = 'news-archive_year'
    ),
    # news archive month list
    url(
        regex  = '^(?P<year>\d{4})/(?P<month>\w{3})/$',
        view   = 'django.views.generic.date_based.archive_month',
        kwargs = info_dict,
        name   = 'news-archive_month'
    ),
    # news archive week list
    url(
        regex  = '^(?P<year>\d{4})/(?P<week>\d{1,2})/$',
        view   = 'django.views.generic.date_based.archive_week',
        kwargs = info_dict,
        name   = 'news-archive_week'
    ),
    # news archive day list
    url(
        regex  = '^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/$',
        view   = 'django.views.generic.date_based.archive_day',
        kwargs = info_dict,
        name   = 'news-archive_day'
    ),
    url(
        regex  = '^today/$',
        view   = 'django.views.generic.date_based.archive_today',
        kwargs = info_dict,
        name   = 'news-archive_day'
    ),
    url(
        regex  = '^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[\w_-]+)/$',
        view   = 'django.views.generic.date_based.archive_day',
        kwargs = dict(info_dict,slug_field="slug"),
        name   = 'news-archive_day'
    ),
)
