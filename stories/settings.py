#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Provides the default settings for the news app
"""

import warnings

from django.conf import settings
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

DEFAULT_STATUS_CHOICES = (
    (1, _(u'DRAFT')),
    (2, _(u'READY FOR EDITING')),
    (3, _(u'READY TO PUBLISH')),
    (4, _(u'PUBLISHED')),
    (5, _(u'REJECTED')),
    (6, _(u'UN-PUBLISHED')),
)

DEFAULT_ORIGIN_CHOICES = (
    (0, _(u'Admin')),
)

DEFAULT_PAGINATION = {
    'PAGINATE': False,
    'P_PER_PAGE': 20,
    'ORPHANS': 4
}
DEFAULT_QUICKEDIT_FIELDS = (
    'headline',
    'subhead',
    'kicker',
    'status',
    'teaser'
)

DEFAULT_SETTINGS = {
    'AUTHOR_MODEL': 'auth.User',
    'AUTHOR_MODEL_LIMIT_CHOICES': {'is_staff': True},
    'DEFAULT_ORIGIN': 0,
    'DEFAULT_STATUS': 1,
    'ADMIN_EXTRAS': {
        'EXTRA_FIELDSETS': (),
        'RAW_ID_FIELDS': (),
        'FILTER_HORIZONTAL_FIELDS': ('authors',),
        'SEARCH_FIELDS': ('headline',),
        'LIST_PER_PAGE': 25,
    },
    'INCLUDE_PRINT': False,
    'ORDERING': ['-publish_date'],
    'ORIGIN_CHOICES': DEFAULT_ORIGIN_CHOICES,
    'PAGINATION': DEFAULT_PAGINATION,
    'PUBLISHED_STATUS': 4,
    'QUICKEDIT_FIELDS': DEFAULT_QUICKEDIT_FIELDS,
    'RELATION_MODELS': [],
    'STATUS_CHOICES': DEFAULT_STATUS_CHOICES,
    'THROW_404': True,
    'USE_REVERSION': False,
    'WIDGET': None,
    'WIDGET_ATTRS': None,
    'WIDGET_FIELDS': ['body', ]
}

USER_SETTINGS = getattr(settings, 'STORY_SETTINGS', {})

DEFAULT_SETTINGS.update(USER_SETTINGS)

COMMENTS_DISABLED = 0
COMMENTS_ENABLED = 1
COMMENTS_FROZEN = 2

COMMENT_STATUSES = (
    (COMMENTS_DISABLED, _('Comments Disabled')),
    (COMMENTS_ENABLED, _('Comments Enabled')),
    (COMMENTS_FROZEN, _('Comments Frozen'))
)

RELATIONS = [Q(app_label=al, model=m) for al, m in [x.split('.') for x in DEFAULT_SETTINGS['RELATION_MODELS']]]

if 'STORY_ORDERING' in DEFAULT_SETTINGS:
    warnings.warn('STORY_ORDERING is being deprecated; use ORDERING instead.', DeprecationWarning)
    DEFAULT_SETTINGS['ORDERING'] = DEFAULT_SETTINGS.pop('STORY_ORDERING')

globals().update(DEFAULT_SETTINGS)
globals().update({'RELATIONS': RELATIONS})
