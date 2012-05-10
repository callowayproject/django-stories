"""This module provides the Story model for reporting news
"""
import diff_match_patch
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from datetime import datetime
from django.contrib.sites.models import Site

# pylint: disable-msg=E0611
from settings import (STATUS_CHOICES, PUBLISHED_STATUS, DEFAULT_STATUS, 
    ORIGIN_CHOICES, DEFAULT_ORIGIN, RELATION_MODELS, RELATIONS, INCLUDE_PRINT,
    USE_CATEGORIES, USE_REVERSION, AUTHOR_MODEL, AUTHOR_MODEL_LIMIT_CHOICES,
    STORY_ORDERING )

if USE_CATEGORIES:
    from categories.fields import CategoryM2MField, CategoryFKField

COMMENT_STATUSES = (
    (1, _('Comments Enabled')),
    (0, _('Comments Disabled')),
    (2, _('Comments Frozen'))
)

DMP = diff_match_patch.diff_match_patch()

def diff(txt1, txt2):
    """Create a 'diff' from txt1 to txt2."""
    patch = DMP.patch_make(txt1, txt2)
    return DMP.patch_toText(patch)

class CurrentSitePublishedManager(models.Manager):
    def get_query_set(self):
        queryset = super(CurrentSitePublishedManager, self).get_query_set()
        return queryset.filter(
            publish_date__lte=datetime.now()).filter(
                status__exact=PUBLISHED_STATUS)

class Story(models.Model):
    """
    A newspaper or magazine type story or document that was possibly also printed
    in a periodical.
    """
    headline = models.CharField(_("Headline"), 
        max_length=100)
    tease_headline = models.CharField(_("Tease Headline"), 
        max_length=100,
        default="",
        blank=True)
    subhead = models.CharField(_("Subheadline"), 
        max_length=200, 
        blank=True, 
        null=True)
    slug = models.SlugField(_('Slug'), 
        max_length=50)
    authors = models.ManyToManyField(AUTHOR_MODEL, 
        verbose_name=_('Authors'), 
        blank=True, 
        null=True,
        limit_choices_to=AUTHOR_MODEL_LIMIT_CHOICES)
    non_staff_author = models.CharField(_('Non-staff author(s)'), 
        max_length=200, 
        blank=True, 
        null=True,
        help_text=_("An HTML-formatted rendering of an author(s) not on staff."))
    publish_date = models.DateField(_('Publish Date'),
        help_text=_("The date the original story was published"), 
        blank=True, 
        null=True)
    publish_time = models.TimeField(_('Publish Time'),
        help_text=_("The time the original story was published"), 
        blank=True, 
        null=True)
    update_date = models.DateTimeField(_('Update Date'), 
        help_text=_("The update date/time to display to the user"), 
        blank=True, 
        null=True)
    modified_date = models.DateTimeField(_("Date Modified"), 
        auto_now=True, 
        blank=True, 
        editable=False)
    if INCLUDE_PRINT:
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
    comment_status = models.IntegerField(_('Comment Status'),
        choices=COMMENT_STATUSES,
        default=1
    )
    status = models.IntegerField(_('Published Status'), 
        choices=STATUS_CHOICES, 
        default=DEFAULT_STATUS)
    teaser = models.TextField(_("Teaser Text"), blank=True)
    kicker = models.CharField(_('Kicker'), 
        max_length=50, 
        blank=True, 
        null=True)
    body = models.TextField(_("Body"))
    origin = models.IntegerField(_("Origin"),
        choices=ORIGIN_CHOICES,
        default=DEFAULT_ORIGIN,)
    site = models.ForeignKey(Site, verbose_name=_('Site'))
    
    if USE_CATEGORIES:
        primary_category = CategoryFKField(related_name='primary_story_set')
        categories = CategoryM2MField(blank=True)
    
    objects = models.Manager()
    published = CurrentSitePublishedManager()
    
    class Meta:
        verbose_name = _("Story")
        verbose_name_plural = _("Stories")
        ordering = STORY_ORDERING
        get_latest_by = 'publish_date'
        unique_together = ('publish_date','slug')
    
    @models.permalink
    def get_absolute_url(self):
        return ('news_detail', (
            self.publish_date.year,
            self.publish_date.strftime('%b').lower(),
            self.publish_date.day,
            self.slug
        )) 
    @property
    def comments_frozen(self):
        """
        Simplified way to get the comment status == frozen
        """
        return self.comment_status == 2
    
    @property
    def author(self):
        """
        Easy way to get a combination of authors without having to worry which
        fields are set (author/one-off author)
        """
        AuthorModel = models.get_model(*AUTHOR_MODEL.split("."))
        link = '<a href="%s">%s %s</a>'
        if AuthorModel.__module__ == 'django.contrib.auth.models':
            authors = [link % (
                i.get_profile().get_absolute_url(), 
                i.first_name, 
                i.last_name) for i in self.authors.all()]
        else:
            authors = [link % (i.get_absolute_url(), i.first_name, i.last_name)
                       for i in self.authors.all()]
        if self.non_staff_author:
            authors.append(self.non_staff_author)
        if len(authors) > 1:
            author_string = "%s and %s" % (", ".join(authors[:-1]), authors[-1])
        elif len(authors) == 1:
            author_string = authors[0]
        else:
            author_string = ''
        return mark_safe(author_string)
    
    @property
    def paragraphs(self):
        """
        Return the paragraphs as a list
        """
        import re
        
        return re.findall("(<p>.+?</p>)", self.body, re.I | re.S)
    
    if RELATION_MODELS:
        def get_related_content_type(self, content_type):
            """
            Get all related items of the specified content type
            """
            return self.storyrelation_set.filter(
                content_type__name=content_type)
        
        def get_relation_type(self, relation_type):
            """
            Get all relations of the specified relation type
            """
            return self.storyrelation_set.filter(relation_type=relation_type)
    
    def __unicode__(self):
        return "%s : %s" % (self.headline, self.publish_date)


if RELATION_MODELS:
    STORY_RELATION_LIMITS = reduce(lambda x, y: x|y, RELATIONS)
    class StoryRelationManager(models.Manager):
        """Basic manager with a few convenience methods"""
        def get_content_type(self, content_type):
            """
            Get all the related items with a specific content_type
            """
            qs = self.get_query_set()
            return qs.filter(content_type__name=content_type)
        
        def get_relation_type(self, relation_type):
            """
            Get all the related items with a specific relation_type
            """
            qs = self.get_query_set()
            return qs.filter(relation_type=relation_type)
    
    
    class StoryRelation(models.Model):
        """Related story item"""
        story = models.ForeignKey(Story)
        content_type = models.ForeignKey(
            ContentType, 
            limit_choices_to=STORY_RELATION_LIMITS)
        object_id = models.PositiveIntegerField()
        content_object = generic.GenericForeignKey('content_type', 'object_id')
        relation_type = models.CharField(_("Relation Type"), 
            max_length="200", 
            blank=True, 
            null=True,
            help_text=_(
                "A generic text field to tag a relation, like 'leadphoto'."))
        
        objects = StoryRelationManager()
        
        def __unicode__(self):
            return unicode(self.content_object)


# Reversion integration
if USE_REVERSION:
    import reversion
    try:
        reversion.register(Story)
    except:
        pass
