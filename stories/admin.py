import os
from django.contrib import admin
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from genericcollection import *

from models import Story, StoryRelation
from forms import StoryForm


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
    filter_horizontal = ('authors',)
    inlines = [InlineStoryRelation,]
    fieldsets = (
        (None,{
            'fields': ('headline', 'subhead', 'authors', 'non_staff_author', 'teaser', 'body')
        }), 
        ('Story data', {
            'fields': ('status', 'comments', )
        }),
        ('Additional Story Info', {
            'fields': ('source', 'post_story_blurb', 'origin'),
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
        js = ('js/genericcollections.js')

admin.site.register(Story, StoryOptions)
