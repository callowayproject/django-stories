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
    markup = forms.CharField(max_length=3, 
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



class InlineStoryRelation(GenericCollectionTabularInline):
    model = StoryRelation


class StoryOptions(admin.ModelAdmin):
    form = StoryForm
    list_display = ('headline', 'status', 'publish_date', 'modified_date')
    list_filter = ('site', 'publish_date')
    search_fieldsets = ('headline', 'summary', 'body')
    date_hierarchy = 'publish_date'
    list_per_page = 25
    prepopulated_fields = {'slug': ('headline',)}
    filter_horizontal = ('authors','categories',)
    inlines = [InlineStoryRelation,]
    fieldsets = (
        (None,{
            'fields': ('headline', 'subhead', 'authors', 'non_staff_author')
        }),
        ('Content',{
            'fields': ('teaser', 'body', 'markup',)
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
            '/media/js/genericcollections.js', 
            '/media/fckeditor/fckeditor.js',
            '/media/fckeditor/fckareas.js'
        )

admin.site.register(Story, StoryOptions)
