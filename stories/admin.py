from models import Story, StoryRelation
from categories.models import Category
from django import forms
from django.contrib import admin
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from genericcollection import *
from django.forms.util import ErrorList
import os
from mptt.forms import TreeNodeChoiceField
    
from settings import MARKUP_CHOICES

class StoryForm(forms.ModelForm):
    markup = forms.CharField(max_length=3, required=False,
                             widget=forms.Select(choices=MARKUP_CHOICES, 
                             attrs={'onchange':'changeMarkup(this)'}))
    primary_category = TreeNodeChoiceField(queryset=Story.objects.get_category_list(),
                                            level_indicator=u'+-')
    class Meta:
        model = Story
    
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                     initial=None, error_class=ErrorList, label_suffix=':',
                     empty_permitted=False, instance=None):
        # Set a default publish time and the current site if it is a new object
        import datetime
        from django.contrib.sites.models import Site        
        if not instance and (initial is not None and not initial.has_key('publish_date')):
            initial['publish_date'] = datetime.datetime.now()
        if not instance and (initial is not None and not initial.has_key('site')):
            initial['site'] = [Site.objects.get_current().id,]
        super(StoryForm, self).__init__(data, files, auto_id, prefix, initial, 
                                        error_class, label_suffix, 
                                        empty_permitted, instance)
                                        
    def save(self, **kw):
        # 1 - Get the old stuff before saving
        if self.instance.id is None:
            old_headline = old_body = old_markup = ''
            new = True
        else:
            old_headline = self.instance.headline
            old_body = self.instance.body
            old_markup = self.instance.markup
            new = False

        # 2 - Save the Article
        story = super(StoryForm, self).save(**kw)

        # 3 - Set creator
        # editor = getattr(self, 'editor', None)
        if new:
            # if editor is not None:
            #     article.creator = editor
            #     article.group = group
            story.save()

        # 4 - Create new revision
        if not old_body == story.body:
            changeset = story.new_revision(
                old_body, old_headline, old_markup, None)

        return story#, changeset



class InlineStoryRelation(GenericCollectionTabularInline):
    model = StoryRelation
    exclude = ('relation_type',)


class StoryOptions(admin.ModelAdmin):
    form = StoryForm
    list_display = ('headline', 'status', 'publish_date', 'modified_date')
    list_filter = ('site', 'publish_date')
    search_fields = ('headline', 'teaser', 'body')
    date_hierarchy = 'publish_date'
    list_per_page = 25
    prepopulated_fields = {'slug': ('headline',)}
    filter_horizontal = ('authors','categories',)
    inlines = [InlineStoryRelation,]
    fieldsets = (
        (None,{
            'fields': ('headline', 'subhead', 'authors', 'non_staff_author', 'teaser', 'body')
        }), 
        ('Story data', {
            'fields': ('status', 'primary_category', 'comments', )
        }),
        ('Additional Story Info', {
            'fields': ('source', 'post_story_blurb', 'origin', 'categories',),
            'classes': ('collapse',),
        }),
        # ('Print Information', {
        #     'fields': ('print_pub_date', 'print_section', 'print_page'),
        #     'classes': ('collapse',),
        # }),
        ('Advanced Options',{
            'fields': ('slug','publish_date', 'update_date', 'site', ),
            'classes': ('collapse',),
        })
    )
    class Media:
        js = (
        )

admin.site.register(Story, StoryOptions)
