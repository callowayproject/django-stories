#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

from django import forms
from django.contrib.sites.models import Site
from django.utils.translation import ugettext as _

from .models import Story

WIDGET_ATTRS = {'size': '85'}

class StoryForm(forms.ModelForm):
    headline = forms.CharField(
        widget=forms.TextInput(attrs=WIDGET_ATTRS),
        max_length=100)
    subhead = forms.CharField(
        widget=forms.TextInput(attrs=WIDGET_ATTRS),
        max_length=200,
        required=False)
    tease_headline = forms.CharField(
        widget=forms.TextInput(attrs=WIDGET_ATTRS),
        max_length=100, required=False)
    kicker = forms.CharField(
        widget=forms.TextInput(attrs=WIDGET_ATTRS),
        max_length=50, required=False)
    non_staff_author = forms.CharField(
        widget=forms.TextInput(attrs=WIDGET_ATTRS),
        help_text=_('An HTML-formatted rendering of the author(s) not on staff.'),
        max_length=200,
        required=False)

    class Meta:
        model = Story

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        instance = kwargs.get('instance', None)

        # Set a default publish time and the current site if it is a new object
        if not instance and not 'publish_date' in initial:
            initial['publish_date'] = datetime.datetime.now().date()
        if not instance and not 'publish_time' in initial:
            initial['publish_time'] = datetime.datetime.now().time().strftime('%H:%M:%S')
        if not instance and not 'site' in initial:
            initial['site'] = Site.objects.get_current().id

        kwargs.update({'initial': initial})
        super(StoryForm, self).__init__(*args, **kwargs)

    def clean_slug(self):
        """The slug + the publish_date must be unique together"""

        if 'publish_date' in self.cleaned_data:
            publish_date = self.cleaned_data['publish_date']
            try:
                Story.objects.get(
                    slug=self.cleaned_data['slug'],
                    publish_date__year=publish_date.year,
                    publish_date__month=publish_date.month,
                    publish_date__day=publish_date.day)
                raise forms.ValidationError(
                    'Please enter a different slug. The one you'\
                    'entered is already being used for {0}'.format(
                         publish_date.strftime("%Y-%b-%d")))
            except Story.DoesNotExist:
                pass

        return self.cleaned_data['slug']
