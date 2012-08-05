#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime, time

from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import EmptyPage, InvalidPage
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from stories import settings
from .models import Story
from .paragraph_paginator import ParagraphPaginator


@staff_member_required
def admin_changeset_list(request, story_id,
    template_name='admin/stories/changesets.html'):
    try:
        story = Story.objects.get(pk=story_id)
    except Story.DoesNotExist:
        raise Http404

    chsets = story.changeset_set.all().order_by('-revision')


    return render_to_response(template_name,
                              {'story': story,
                               'changesets': chsets},
                              context_instance=RequestContext(request))

@staff_member_required
def admin_changeset_revert(request, story_id, revision_id,
    template_name='admin/stories/changeset_revert.html'):

    try:
        story = Story.objects.get(pk=story_id)
    except Story.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        if 'confirm' in request.POST:
            story.revert_to(revision_id)
            return HttpResponseRedirect('../../')
        elif 'cancel' in request.POST:
            return HttpResponseRedirect('../../changesets/')

    changeset = story.changeset_set.get(revision=revision_id)

    return render_to_response(template_name,
                              {'story': story,
                               'changeset': changeset},
                              context_instance=RequestContext(request))

def pag_story_detail(request, year, month, day, slug,
        p_per_page=settings.PAGINATION['P_PER_PAGE'],
        orphans=settings.PAGINATION['ORPHANS'],
        p_object_name="story_content", template_object_name="story",
        template_name="stories/pag_story.html", extra_context={}):
    """
    A detail view for stories that paginates the story by paragraph
    """
    try:
        pub_date = datetime.date(*time.strptime(year+month+day, '%Y%b%d')[:3])
    except ValueError:
        raise Http404

    qs = Story.published.get
    if request.user.is_staff:
        qs = Story.objects.get

    try:
        story = qs(publish_date=pub_date, slug=slug)
    except Story.DoesNotExist:
        if not settings.THROW_404:
            return render_to_response('stories/story_removed.html',
                                      {},
                                      context_instance=RequestContext(request))
        else:
            raise Http404

    if settings.PAGINATION['PAGINATE']:
        paginator = ParagraphPaginator(story.body, p_per_page, orphans=orphans)

        # Make sure page request is an int. If not, deliver first page.
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1

        try:
            story_content = paginator.page(page)
        except (EmptyPage, InvalidPage):
            story_content = paginator.page(paginator.num_pages)
    else:
        story_content = story.body

        # If the default template hasn't been changed, use the non-pagination
        # template
        if template_name == "stories/pag_story.html":
            template_name = "stories/story_detail.html"

    context = {p_object_name: story_content,
               template_object_name: story}
    if extra_context:
        context.update(extra_context)

    return render_to_response(template_name, context,
                              context_instance=RequestContext(request))

