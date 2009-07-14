"""This module provides the Story model for reporting news
"""
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink
from datetime import datetime
from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.sites.models import Site
from categories.models import Category
try:
    from staff.models import Staff as AuthorModel
except ImportError:
    from django.contrib.auth.models import User as AuthorModel

from settings import MARKUP_CHOICES, STATUS_CHOICES, PUBLISHED_STATUS, \
                    DEFAULT_STATUS, DEFAULT_MARKUP, ORIGIN_CHOICES, \
                    DEFAULT_ORIGIN, CATEGORY_TREE


class CurrentSitePublishedManager(CurrentSiteManager):
    def get_query_set(self):
        queryset = super(CurrentSitePublishedManager, self).get_query_set()
        return queryset.filter(publish_date__lte=datetime.now()).filter(status__exact=PUBLISHED_STATUS)

class StoryManager(models.Manager):
    def get_category_list(self):
        if CATEGORY_TREE:
            return Category.objects.get(name=CATEGORY_TREE, parent__isnull=True).get_children()
        return Category.tree.all()

class Story(models.Model):
    headline = models.CharField(_("Headline"), 
        max_length=100)
    subhead = models.CharField(_("Subheadline"), 
        max_length=200, 
        blank=True, 
        null=True)
    slug = models.SlugField(_('Slug'), 
        max_length=30)
    authors = models.ManyToManyField(AuthorModel, 
        verbose_name=_('Authors'), 
        blank=True, 
        null=True)
    non_staff_author = models.CharField(_('Non-staff author(s)'), 
        max_length=200, 
        blank=True, 
        null=True,
        help_text=_("An HTML-formatted rendering of the author(s)."))
    publish_date = models.DateTimeField(_('Time to Publish'))
    update_date = models.DateTimeField(_('Update Date'), 
        help_text=_("The update date to display to the user"), 
        blank=True, 
        null=True)
    modified_date = models.DateTimeField(_("Date Modified"), 
        auto_now=True, 
        blank=True, 
        editable=False)
    print_pub_date = models.DateTimeField(_('Print Publish Date'),
        blank=True,
        null=True), 
    print_section = models.CharField(_('Print Section'), 
        max_length=30,
        blank=True,
        null=True),
    print_page = models.CharField(_('Print Page'), 
        max_length=5,
        blank=True,
        null=True),
    comments = models.BooleanField(_('Enable Comments?'), 
        default=True)
    status = models.IntegerField(_('Published Status'), 
        choices=STATUS_CHOICES, 
        default=DEFAULT_STATUS)
    source = models.CharField(_("Other Story Sources"), 
        max_length=200,
        blank=True, 
        null=True,)
    teaser = models.TextField(_("Teaser Text"))
    body = models.TextField(_("Body"))
    markup = models.IntegerField(_(u"Content Markup"), 
        choices=MARKUP_CHOICES, 
        default=DEFAULT_MARKUP)
    post_story_blurb = models.CharField(_('Post-story Blurb'), 
        max_length=300, 
        blank=True, 
        help_text='Example: "John Smith contributed to this story."')
    origin = models.IntegerField(_("Origin"),
        choices=ORIGIN_CHOICES,
        default=DEFAULT_ORIGIN,)
    primary_category = models.ForeignKey(Category, 
        verbose_name=_('Primary Category'),
        related_name='primary_category')
    categories = models.ManyToManyField(Category, 
        verbose_name=_('Categories'), 
        blank=True, 
        null=True)
    site = models.ManyToManyField(Site, verbose_name=_('Sites'))
    
    objects = StoryManager()
    published = CurrentSitePublishedManager()
    
    class Meta:
        verbose_name = _("Story")
        verbose_name_plural = _("Stories")
        ordering = ['-publish_date']
        get_latest_by = 'publish_date'
        unique_together = ('publish_date','slug')
    
    def get_absolute_url(self):
        return ('story_detail', (), {
            'section':self.section,
            'year':self.pub_date.year,
            'month':self.pub_date.strftime('%b').lower(),
            'day':self.pubish_date.day,
            'slug':self.slug
        }) 
    get_absolute_url = permalink(get_absolute_url)
    
    def __unicode__(self):
        return "%s : %s" % (self.headline, self.publish_date)

story_relation_limits = {'model__in':('story', 'photo', 'gallery')}
class StoryRelation(models.Model):
    """Related story item"""
    story = models.ForeignKey(Story)
    content_type = models.ForeignKey(ContentType, limit_choices_to=story_relation_limits)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    relation_type = models.IntegerField(_("Relation Type"))

    def __unicode__(self):
        return u"StoryRelation"
