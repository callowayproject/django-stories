#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.conf import settings as site_settings
from django.contrib import admin
from django.forms.models import modelformset_factory, modelform_factory
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import curry

from stories import settings
from .forms import StoryForm
from .models import Story
from .utils import load_widget

HAS_RELATIONS = 'stories.relations' in site_settings.INSTALLED_APPS and settings.RELATIONS

if HAS_RELATIONS:
    from stories.relations.genericcollection import GenericCollectionTabularInline
    from stories.relations.models import StoryRelation

    class InlineStoryRelation(GenericCollectionTabularInline):
        model = StoryRelation

if settings.USE_REVERSION:
    from reversion.admin import VersionAdmin
    AdminModel = VersionAdmin
else:
    AdminModel = admin.ModelAdmin


class ChangeStatus(object):
    """A class to create objects that can dynamically set status
       from the admin"""
    def __init__(self, status_val, status_name):
        super(ChangeStatus, self).__init__()
        self.status_val = status_val
        self.status_name = status_name.__unicode__()
        self.__name__ = "set_status_to_%s" % self.status_name

    def __call__(self, modeladmin, request, queryset):
        rows_updated = queryset.update(status=self.status_val)
        if rows_updated == 1:
            message_bit = "1 story was"
        else:
            message_bit = "%s stories were" % rows_updated
        modeladmin.message_user(request,
            "%s successfully marked as %s." % (
                message_bit, self.status_name))


admin_actions = [ChangeStatus(x, y) for x, y in settings.STATUS_CHOICES]


class StoryAdmin(AdminModel):
    """
    The story admin

    Some attributes are set based on `settings`, such as
    fieldsets and filter_horizontal. Below is a list of
    all the attributes that might be different.
        - list_filter
        - filter_horizontal
        - fieldsets
        - inlines

    A custom queryset is used here so all the stories show up
    in the admin changelist/changeform. This is because the
    default manager supplied on the model defaults to only
    published objects.

    A custom changelist formset is used to supply a subset of
    fields for quick edit. This is used in conjuctions with
    the custom attribute `quick_editable`, which is a list of
    fields.
    """
    list_display = ('headline', 'status', 'publish_date',
                    'modified_date', 'origin')
    list_filter = ('site', 'publish_date', 'origin')
    list_per_page = settings.ADMIN_EXTRAS.get('LIST_PER_PAGE', 25)

    list_editable = ()
    quick_editable = settings.QUICKEDIT_FIELDS

    search_fields = settings.ADMIN_EXTRAS.get('SEARCH_FIELDS', ('headline',))
    date_hierarchy = 'publish_date'
    prepopulated_fields = {'slug': ('headline',)}

    form = StoryForm

    actions = admin_actions
    actions_on_bottom = True

    raw_id_fields = settings.ADMIN_EXTRAS.get('RAW_ID_FIELDS', ())

    filter_horizontal = settings.ADMIN_EXTRAS.get(
        'FILTER_HORIZONTAL_FIELDS', ('authors',))

    if HAS_RELATIONS:
        inlines = [InlineStoryRelation, ]

    fieldsets = (
        (None, {
            'fields': ('headline', 'subhead', 'tease_headline',
                       'teaser', 'body')
        }),
        (_('Story data'), {
            'fields': ('kicker', 'authors', 'non_staff_author',
                       'status', 'origin', 'comment_status', )
        }),)

    if settings.INCLUDE_PRINT:
        fieldsets = fieldsets + (_('Print Information'), {
            'fields': ('print_pub_date', 'print_section', 'print_page'),
            'classes': ('collapse',),
        })

    fieldsets = fieldsets + ((_('Advanced Options'), {
            'fields': ('slug', ('publish_date', 'publish_time'),
                       'update_date', 'site', ),
            'classes': ('collapse',),
        }),)

    change_list_template = 'admin/stories/change_list.html'
    revision_form_template = 'admin/stories/reversion_form.html'

    class Media:
        js = ('js/quickedit.js',)
        if HAS_RELATIONS:
            js += ('js/genericcollections.js',)

        css = {'all': ('css/quickedit.css',)}

    def __init__(self, *args, **kwargs):
        super(StoryAdmin, self).__init__(*args, **kwargs)

        # Add in any extra fielsets
        self.fieldsets = list(self.fieldsets)
        for extra_fs in settings.ADMIN_EXTRAS.get('EXTRA_FIELDSETS', ()):
            fs = (extra_fs.get('name', None), {
                    'fields': extra_fs['fields'],
                    'classes': extra_fs.get('classes', ()),
                    'description': extra_fs.get('description', None)
                 })

            if 'position' in extra_fs:
                self.fieldsets.insert(extra_fs.get('position'), fs)
            else:
                self.fieldsets.append(fs)

    def _get_widget(self):
        attrs = settings.WIDGET_ATTRS
        widget = load_widget(settings.WIDGET) or forms.Textarea
        return widget(attrs=attrs)

    def formfield_for_dbfield(self, db_field, **kwargs):
        """Supply the widget to the body field"""
        if db_field.name in settings.WIDGET_FIELDS:
            return db_field.formfield(widget=self._get_widget())
        return super(StoryAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    def queryset(self, request):
        """
        Need to override to show all the stories. Default manager
        only shows published stories
        """
        qs = self.model.objects.get_query_set()
        ordering = self.ordering or ()  # otherwise we might try to *None, which is bad ;)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def changelist_view(self, *args, **kwargs):
        self.list_editable = True
        return super(StoryAdmin, self).changelist_view(*args, **kwargs)

    def get_changelist_formset(self, request, **kwargs):
        """
        Returns the quickedit formset for the row
        """
        defaults = {
            'formfield_callback': curry(
                self.formfield_for_dbfield,
                request=request),
        }
        defaults.update(kwargs)
        QEForm = modelform_factory(self.model)
        return modelformset_factory(
            self.model,
            QEForm,
            extra=0,
            fields=self.quick_editable,
            **defaults)


admin.site.register(Story, StoryAdmin)
