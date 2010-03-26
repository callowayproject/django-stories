import os
from django.contrib import admin
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from genericcollection import *

from models import Story
from stories.settings import RELATION_MODELS, INCLUDE_PRINT, STATUS_CHOICES
from forms import StoryForm


if RELATION_MODELS:
    from models import StoryRelation

    class InlineStoryRelation(GenericCollectionTabularInline):
        model = StoryRelation
        # exclude = ('relation_type',)

if 'reversion' in settings.INSTALLED_APPS:
    from reversion.admin import VersionAdmin
    AdminModel = VersionAdmin
else:
    AdminModel = admin.ModelAdmin

HAS_CATEGORIES = 'categories' in settings.INSTALLED_APPS

class ChangeStatus(object):
    """A class to create objects that can dynamically set status from the admin"""
    def __init__(self, status_val, status_name):
        super(ChangeStatus, self).__init__()
        self.status_val = status_val
        self.status_name = status_name.__unicode__()
        self.__name__ = "set_status_to_%s" % self.status_name
    
    def __call__(self, admin, request, queryset):
        rows_updated = queryset.update(status=self.status_val)
        if rows_updated == 1:
            message_bit = "1 story was"
        else:
            message_bit = "%s stories were" % rows_updated
        admin.message_user(request, "%s successfully marked as %s." % (message_bit, self.status_name))

admin_actions = [ChangeStatus(x,y) for x, y in STATUS_CHOICES]

class StoryOptions(AdminModel):
    revision_form_template = "admin/stories/reversion_form.html"
    form = StoryForm
    list_display = ('headline', 'status', 'publish_date', 'modified_date')
    list_filter = ('site', 'publish_date')
    search_fields = ('headline', 'teaser', 'body')
    date_hierarchy = 'publish_date'
    list_per_page = 25
    prepopulated_fields = {'slug': ('headline',)}
    filter_horizontal = ('authors',)
    actions = admin_actions
    if RELATION_MODELS:
        inlines = [InlineStoryRelation,]
    fieldsets = (
        (None,{
            'fields': ('headline', 'subhead', 'teaser', 'body')
        }), 
        ('Story data', {
            'fields': ('kicker', 'authors', 'non_staff_author', 'status', 'comments', )
        }),)
    if HAS_CATEGORIES:
        fieldsets = fieldsets + (
            ('Categories', {
                'fields': ('primary_category','categories')
            }),
        )
    if INCLUDE_PRINT:
        fieldsets = fieldsets + ('Print Information', {
            'fields': ('print_pub_date', 'print_section', 'print_page'),
            'classes': ('collapse',),
        })
    fieldsets = fieldsets + (('Advanced Options',{
            'fields': ('origin','slug',('publish_date', 'publish_time'), 'update_date', 'site', ),
            'classes': ('collapse',),
        }),)
    
    class Media:
        js = ('js/genericcollections.js',)


admin.site.register(Story, StoryOptions)
