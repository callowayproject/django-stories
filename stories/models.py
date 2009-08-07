"""This module provides the Story model for reporting news
"""
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.conf import settings
from django.utils.translation import ugettext as _
from datetime import datetime
from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.sites.models import Site
from categories.models import Category
try:
    from staff.models import StaffMember as AuthorModel
except ImportError:
    from django.contrib.auth.models import User as AuthorModel

from settings import MARKUP_CHOICES, STATUS_CHOICES, PUBLISHED_STATUS, \
                    DEFAULT_STATUS, DEFAULT_MARKUP, ORIGIN_CHOICES, \
                    DEFAULT_ORIGIN, CATEGORY_TREE

import diff_match_patch

dmp = diff_match_patch.diff_match_patch()

def diff(txt1, txt2):
    """Create a 'diff' from txt1 to txt2."""
    patch = dmp.patch_make(txt1, txt2)
    return dmp.patch_toText(patch)

#class CurrentSitePublishedManager(CurrentSiteManager):
class CurrentSitePublishedManager(models.Manager):
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
    site = models.ForeignKey(Site, verbose_name=_('Site'))
    
    objects = StoryManager()
    published = CurrentSitePublishedManager()
    
    class Meta:
        verbose_name = _("Story")
        verbose_name_plural = _("Stories")
        ordering = ['-publish_date']
        get_latest_by = 'publish_date'
        unique_together = ('publish_date','slug')
    
    def get_absolute_url(self):
        return 'http://%s/news/%s/%s/%s/%s' % (
            self.site.domain,
            self.publish_date.year,
            self.publish_date.strftime('%b').lower(),
            self.publish_date.day,
            self.slug
        ) 
    
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
    
    def base(self):
        try:
            from base.models import Base
            return Base.objects.filter(site=self.site)[0]
        except:
            pass
    
    def __unicode__(self):
        return "%s : %s" % (self.headline, self.publish_date)
    
    # Borrowed from wiki-app
    # http://code.google.com/p/django-wikiapp/
    def latest_changeset(self):
        try:
            return self.changeset_set.filter(
                reverted=False).order_by('-revision')[0]
        except IndexError:
            return ChangeSet.objects.none()

    def new_revision(self, old_body, old_headline, old_markup, editor):
        '''Create a new ChangeSet with the old content.'''

        content_diff = diff(self.body, old_body)

        cs = ChangeSet.objects.create(
            story=self,
            editor=editor,
            old_headline=old_headline,
            old_markup=old_markup,
            content_diff=content_diff)

        # TODO: Notification

        return cs

    def revert_to(self, revision, editor=None):
        """ Revert the story to a previuos state, by revision number.
        """
        changeset = self.changeset_set.get(revision=revision)
        changeset.reapply(editor)
        

story_relation_limits = {'model__in':('story', 'photo', 'gallery')}
class StoryRelation(models.Model):
    """Related story item"""
    story = models.ForeignKey(Story)
    content_type = models.ForeignKey(ContentType, limit_choices_to=story_relation_limits)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    relation_type = models.IntegerField(_("Relation Type"), blank=True, null=True)

    def __unicode__(self):
        return u"StoryRelation"


# Borrowed from wiki-app
# http://code.google.com/p/django-wikiapp/

class ChangeSetManager(models.Manager):

    def all_later(self, revision):
        """ Return all changes later to the given revision.
        Util when we want to revert to the given revision.
        """
        return self.filter(revision__gt=int(revision))


class NonRevertedChangeSetManager(ChangeSetManager):

    def get_default_queryset(self):
        super(PublishedBookManager, self).get_query_set().filter(
            reverted=False)


class ChangeSet(models.Model):
    """A report of an older version of some Story."""

    story = models.ForeignKey(Story, verbose_name=_(u"Story"))

    # Editor identification -- logged or anonymous
    editor = models.ForeignKey(AuthorModel, verbose_name=_(u'Editor'),
                               null=True)

    # Revision number, starting from 1
    revision = models.IntegerField(_(u"Revision Number"))

    # How to recreate this version
    old_headline = models.CharField(_(u"Old Headline"), max_length=100, blank=True)
    old_markup = models.CharField(_(u"Story Content Markup"), max_length=3,
                                  choices=MARKUP_CHOICES,
                                  null=True, blank=True)
    content_diff = models.TextField(_(u"Content Patch"), blank=True)

    modified = models.DateTimeField(_(u"Modified at"), default=datetime.now)
    reverted = models.BooleanField(_(u"Reverted Revision"), default=False)

    objects = ChangeSetManager()
    non_reverted_objects = NonRevertedChangeSetManager()

    class Meta:
        verbose_name = _(u'Change set')
        verbose_name_plural = _(u'Change sets')
        get_latest_by  = 'modified'
        ordering = ('-revision',)

    def __unicode__(self):
        return u'#%s' % self.revision

    @models.permalink
    def get_absolute_url(self):
        return ('story_changeset', None, {
            'slug': self.story.slug,
            'revision': self.revision
        })

    def is_anonymous_change(self):
        return self.editor is None

    def reapply(self, editor):
        """ Return the Story to this revision.
        """

        # XXX Would be better to exclude reverted revisions
        #     and revisions previous/next to reverted ones
        next_changes = self.story.changeset_set.filter(
            revision__gt=self.revision).order_by('-revision')

        story = self.story

        content = None
        for changeset in next_changes:
            if content is None:
                content = story.body
            patch = dmp.patch_fromText(changeset.content_diff)
            content = dmp.patch_apply(patch, content)[0]

            changeset.reverted = True
            changeset.save()

        old_body = story.body
        old_headline = story.headline
        old_markup = story.markup

        story.body = content
        story.headline = changeset.old_headline
        story.markup = changeset.old_markup
        story.save()

        story.new_revision(
            old_body=old_body, old_headline=old_headline,
            old_markup=old_markup, editor=editor)

        self.save()

        # TODO: Notification

    def save(self, force_insert=False, force_update=False):
        """ Saves the story with a new revision.
        """
        if self.id is None:
            try:
                self.revision = ChangeSet.objects.filter(
                    story=self.story).latest().revision + 1
            except self.DoesNotExist:
                self.revision = 1
        super(ChangeSet, self).save(force_insert, force_update)

    def display_diff(self):
        ''' Returns a HTML representation of the diff.
        '''

        # well, it *will* be the old content
        old_content = self.story.body

        # newer non-reverted revisions of this story, starting from this
        newer_changesets = ChangeSet.non_reverted_objects.filter(
            story=self.story,
            revision__gte=self.revision)

        # apply all patches to get the content of this revision
        for i, changeset in enumerate(newer_changesets):
            patches = dmp.patch_fromText(changeset.content_diff)
            if len(newer_changesets) == i+1:
                # we need to compare with the next revision after the change
                next_rev_content = old_content
            old_content = dmp.patch_apply(patches, old_content)[0]

        diffs = dmp.diff_main(old_content, next_rev_content)
        return dmp.diff_prettyHtml(diffs)
