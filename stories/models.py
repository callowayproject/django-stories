#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module provides the Story model for reporting news
"""
import re

from datetime import datetime

from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.conf import settings as site_settings
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.db import models
from django.template.loader import select_template
from django.template import Context
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from stories import settings


class CurrentSitePublishedManager(CurrentSiteManager):
    def get_query_set(self):
        queryset = super(CurrentSitePublishedManager, self).get_query_set()
        return queryset.filter(
            publish_date__lte=datetime.now()
        ).filter(
            status__exact=settings.PUBLISHED_STATUS
        )


class AlternateManager(CurrentSiteManager):
    """
    This is the default manager. In some cases, if you only have access to the
    default manager, you can use the published() method to get the right stuff
    """
    def unique_slug(self, publish_date, slug, exclude_id=None):
        """
        Check if the date/slug combination is unique
        """
        query_params = {
            'slug': slug[:50],
            'publish_date': publish_date,
        }
        qset = self.get_query_set().filter(**query_params)
        if exclude_id:
            qset = qset.exclude(id=exclude_id)
        return qset.count() == 0

    def get_unique_slug(self, publish_date, slug, story_id=None):
        """
        Return a unique slug by adding a digit to the end
        """
        query_params = {
            'publish_date__year': publish_date.year,
            'publish_date__month': publish_date.month,
            'publish_date__day': publish_date.day
        }
        if not self.unique_slug(publish_date, slug, story_id):
            # Allow up to 10,000 versions on the same date
            query_params['slug__startswith'] = slug[:46]
            num = self.get_query_set().filter(**query_params).count()
            slug = '%s%s' % (slug[:46], str(num + 1))
        return slug

    def published(self):
        queryset = self.get_query_set()
        return queryset.filter(
            publish_date__lte=datetime.now()
        ).filter(
            status__exact=settings.PUBLISHED_STATUS)


class Story(models.Model):
    """
    A newspaper or magazine type story or document that was possibly also
    printed in a periodical.
    """
    headline = models.CharField(
        _("Headline"),
        max_length=100)
    tease_headline = models.CharField(
        _("Tease Headline"),
        max_length=100,
        default="",
        blank=True)
    subhead = models.CharField(
        _("Subheadline"),
        max_length=200,
        blank=True,
        null=True)
    slug = models.SlugField(
        _('Slug'),
        max_length=50)
    authors = models.ManyToManyField(
        settings.AUTHOR_MODEL,
        verbose_name=_('Authors'),
        blank=True,
        null=True,
        limit_choices_to=settings.AUTHOR_MODEL_LIMIT_CHOICES)
    non_staff_author = models.CharField(
        _('Non-staff author(s)'),
        max_length=200,
        blank=True,
        null=True,
        help_text=_("An HTML-formatted rendering of an author(s) not on staff."))
    publish_date = models.DateField(
        _('Publish Date'),
        help_text=_("The date the original story was published"),
        blank=True,
        null=True)
    publish_time = models.TimeField(
        _('Publish Time'),
        help_text=_("The time the original story was published"),
        blank=True,
        null=True)
    update_date = models.DateTimeField(
        _('Update Date'),
        help_text=_("The update date/time to display to the user"),
        blank=True,
        null=True)
    modified_date = models.DateTimeField(
        _("Date Modified"),
        auto_now=True,
        blank=True,
        editable=False)

    print_pub_date = models.DateTimeField(
        _('Print Publish Date'),
        blank=True,
        null=True),
    print_section = models.CharField(
        _('Print Section'),
        max_length=30,
        blank=True,
        null=True),
    print_page = models.CharField(
        _('Print Page'),
        max_length=5,
        blank=True,
        null=True),

    comments = models.BooleanField(
        _('Enable Comments?'),
        default=True)
    comment_status = models.IntegerField(
        _('Comment Status'),
        choices=settings.COMMENT_STATUSES,
        default=1
    )
    status = models.IntegerField(
        _('Published Status'),
        choices=settings.STATUS_CHOICES,
        default=settings.DEFAULT_STATUS)
    teaser = models.TextField(_("Teaser Text"), blank=True)
    kicker = models.CharField(
        _('Kicker'),
        max_length=50,
        blank=True,
        null=True)
    body = models.TextField(_("Body"))
    origin = models.IntegerField(
        _("Origin"),
        choices=settings.ORIGIN_CHOICES,
        default=settings.DEFAULT_ORIGIN,)
    site = models.ForeignKey(Site, verbose_name=_('Site'))

    objects = AlternateManager()
    published = CurrentSitePublishedManager()

    class Meta:
        verbose_name = _("Story")
        verbose_name_plural = _("Stories")
        ordering = settings.ORDERING
        get_latest_by = 'publish_date'
        unique_together = ('publish_date', 'slug')

    def get_absolute_url(self):
        if self.publish_date is None:
            return ""
        return reverse('news_detail', args=tuple(), kwargs={
            'year': self.publish_date.year,
            'month': self.publish_date.strftime('%b').lower(),
            'day': self.publish_date.day,
            'slug': self.slug
        })

    def save(self, *args, **kwargs):
        """
        Enforce setting of publish date and time if it is published.
        """
        if self.status == settings.PUBLISHED_STATUS:
            if not self.publish_date:
                self.publish_date = datetime.now().date()
            if not self.publish_time:
                self.publish_time = datetime.now().time()
            self.slug = Story.objects.get_unique_slug(self.publish_date, self.slug, self.id)
        super(Story, self).save(*args, **kwargs)

    @property
    def comments_frozen(self):
        """
        Simplified way to get the comment status == frozen
        """
        return self.comment_status == settings.COMMENTS_FROZEN

    @property
    def author(self):
        """
        Easy way to get a combination of authors without having to worry which
        fields are set (author/one-off author)
        """
        import warnings
        warnings.warn('Story.author property is being deprecated, use '
                      '`Story.author_display` instead', DeprecationWarning)

        AuthorModel = models.get_model(*settings.AUTHOR_MODEL.split("."))
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
    def author_display(self):
        """
        Presentation of the story author(s). Renders the template
        `stories/author_display.html` suppling it with the following context

        * **instance** - the story instance
        * **authors** - all the authors (`authors.objects.all()`)
        * **non_staff_author** - text value that can be used in place of `authors`
        """
        template = "stories/author_display.html"
        ctx = Context()
        ctx.update({
            'instance': self,
            'authors': self.authors.all(),
            'non_staff_author': self.non_staff_author
        })
        t = select_template([template])
        return t.render(ctx)

    @property
    def paragraphs(self):
        """
        Return the `story.body` as paragraphs by finding all `<p>` tags
        """
        return re.findall("(<p>.+?</p>)", self.body, re.I | re.S)

    if 'stories.relations' in site_settings.INSTALLED_APPS:
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


# Reversion integration
if settings.USE_REVERSION:
    rev_error_msg = 'Stories excepts django-reversion to be '\
                    'installed and in INSTALLED_APPS'
    try:
        import reversion
        if not 'reversion' in site_settings.INSTALLED_APPS:
            raise ImproperlyConfigured(rev_error_msg)
    except (ImportError, ):
        raise ImproperlyConfigured(rev_error_msg)

    reversion.register(Story)

# If categories is available as well as south migrations
# we need to ensure the post_syncdb signal is setup for
# us from categories. This is only when using django-categories
# <= 1.1.2, which does not setup the signal correctly
try:
    if 'categories' in site_settings.INSTALLED_APPS and \
       'south' in site_settings.INSTALLED_APPS:
        import categories
        from distutils.version import LooseVersion
        categories_version = LooseVersion(categories.__version__)
        compare_version = LooseVersion('1.1.2')
        if categories_version <= compare_version:
            from categories.migration import migrate_app
            from django.db.models.signals import post_syncdb
            post_syncdb.connect(migrate_app)
except (ImportError, ValueError):
    pass
