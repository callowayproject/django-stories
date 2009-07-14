"""Provides the default settings for the news app
"""
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

DEFAULT_STATUS_CHOICES = (
    ('1', 'DRAFT'),
    ('2', 'READY FOR EDITING'),
    ('3', 'READY TO PUBLISH'),
    ('4', 'PUBLISHED'),
    ('5', 'STATIC'),
    ('6', 'REJECTED'),
)
STATUS_CHOICES = getattr(settings, 'STORY_STATUS_CHOICES', DEFAULT_STATUS_CHOICES)

DEFAULT_DEFAULT_STATUS = '1'
DEFAULT_STATUS = getattr(settings, 'STORY_DEFAULT_STATUS', DEFAULT_DEFAULT_STATUS)

DEFAULT_PUBLISHED_STATUS = '4'
PUBLISHED_STATUS = getattr(settings, 'STORY_PUBLISHED_STATUS', DEFAULT_PUBLISHED_STATUS)

DEFAULT_MARKUP_CHOICES = (
    ('0', _(u'None')),
    ('1', _(u'Creole')),
    ('2', _(u'reStructuredText')),
    ('3', _(u'Textile')),
    ('4', _(u'Markdown')),
    ('5', _(u'HTML')),
)
MARKUP_CHOICES = getattr(settings, 'STORY_MARKUP_CHOICES', DEFAULT_MARKUP_CHOICES)

DEFAULT_DEFAULT_MARKUP = 0
DEFAULT_MARKUP = getattr(settings, 'STORY_DEFAULT_MARKUP', DEFAULT_DEFAULT_MARKUP)

DEFAULT_ORIGIN_CHOICES = (
    ('0', _('Admin')),
)
ORIGIN_CHOICES = getattr(settings, 'STORY_ORIGIN_CHOICES', DEFAULT_ORIGIN_CHOICES)

DEFAULT_DEFAULT_ORIGIN = 0
DEFAULT_ORIGIN = getattr(settings, 'STORY_DEFAULT_ORIGIN', DEFAULT_DEFAULT_ORIGIN)

DEFAULT_CATEGORY_TREE = None # By default it will use all the categories
CATEGORY_TREE = getattr(settings, 'STORY_CATEGORY_TREE', DEFAULT_CATEGORY_TREE)