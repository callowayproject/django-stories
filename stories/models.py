"""This module provides the Story model for reporting news
"""
import diff_match_patch
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext as _
from datetime import datetime
from django.contrib.sites.models import Site
from django.conf import settings as global_settings

if 'staff' in global_settings.INSTALLED_APPS:
    from staff.models import StaffMember as AuthorModel
else:
    from django.contrib.auth.models import User as AuthorModel

if 'categories' in global_settings.INSTALLED_APPS:
    HAS_CATEGORIES = True
    from categories.fields import CategoryM2MField, CategoryFKField
else:
    HAS_CATEGORIES = False

from settings import STATUS_CHOICES, PUBLISHED_STATUS, \
                    DEFAULT_STATUS, ORIGIN_CHOICES, DEFAULT_ORIGIN, \
                    RELATION_MODELS, RELATIONS, INCLUDE_PRINT


dmp = diff_match_patch.diff_match_patch()

def diff(txt1, txt2):
    """Create a 'diff' from txt1 to txt2."""
    patch = dmp.patch_make(txt1, txt2)
    return dmp.patch_toText(patch)

class CurrentSitePublishedManager(models.Manager):
    def get_query_set(self):
        queryset = super(CurrentSitePublishedManager, self).get_query_set()
        return queryset.filter(publish_date__lte=datetime.now()).filter(status__exact=PUBLISHED_STATUS)

class Story(models.Model):
    """
    A newspaper or magazine type story or document that was possibly also printed
    in a periodical.
    """
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
        help_text=_("An HTML-formatted rendering of the author(s) not on staff."))
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
    status = models.IntegerField(_('Published Status'), 
        choices=STATUS_CHOICES, 
        default=DEFAULT_STATUS)
    teaser = models.TextField(_("Teaser Text"))
    kicker = models.CharField(_('Kicker'), 
        max_length=50, 
        blank=True, 
        null=True)
    body = models.TextField(_("Body"))
    origin = models.IntegerField(_("Origin"),
        choices=ORIGIN_CHOICES,
        default=DEFAULT_ORIGIN,)
    site = models.ForeignKey(Site, verbose_name=_('Site'))
    
    if HAS_CATEGORIES:
        primary_category = CategoryFKField(related_name='primary_story_set')
        categories = CategoryM2MField(blank=True)
    
    objects = models.Manager()
    published = CurrentSitePublishedManager()
    
    class Meta:
        verbose_name = _("Story")
        verbose_name_plural = _("Stories")
        ordering = ['-publish_date']
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
    def author(self):
        """
        Easy way to get a combination of authors without having to worry which
        fields are set (author/one-off author)
        """
        authors = ["%s %s" % (i.first_name, i.last_name) for i in self.authors.all()]
        authors.append(self.non_staff_author)
        output = ", ".join(authors)
        return output
    
    @property
    def paragraphs(self):
        """
        Return the paragraphs as a list
        """
        import re
        
        return re.findall("(<p>.+?</p>)", self.body, re.I | re.S)
    
    def __unicode__(self):
        return "%s : %s" % (self.headline, self.publish_date)


if RELATION_MODELS:
    story_relation_limits = reduce(lambda x,y: x|y, RELATIONS)
    class StoryRelation(models.Model):
        """Related story item"""
        story = models.ForeignKey(Story)
        content_type = models.ForeignKey(ContentType, limit_choices_to=story_relation_limits)
        object_id = models.PositiveIntegerField()
        content_object = generic.GenericForeignKey('content_type', 'object_id')
        relation_type = models.CharField(_("Relation Type"), 
            max_length="200", 
            blank=True, 
            null=True,
            help_text=_("A generic text field to tag a relation, like 'leadphoto'."))

        def __unicode__(self):
            return u"StoryRelation"


# Reversion integration
if 'reversion' in global_settings.INSTALLED_APPS:
    import reversion
    reversion.register(Story)