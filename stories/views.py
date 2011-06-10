# Create your views here.
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import EmptyPage, InvalidPage
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from stories.models import Story
from paragraph_paginator import ParagraphPaginator
from stories.settings import THROW_404, PAGINATION

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
        p_per_page=PAGINATION['P_PER_PAGE'], orphans=PAGINATION['ORPHANS'], 
        p_object_name="story_content", template_object_name="story", 
        template_name="stories/pag_story.html", extra_context={}):
    """
    A detail view for stories that paginates the story by paragraph
    """
    import datetime, time
    
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
        if not THROW_404:
            return render_to_response('stories/story_removed.html',
                                      {},
                                      context_instance=RequestContext(request))
        else:
            raise Http404
    
    if PAGINATION['PAGINATE']:
        paginator = ParagraphPaginator(story.body, p_per_page, orphans=orphans)
        
        # Make sure page request is an int. If not, deliver first page.
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
        
        # If page request (9999) is out of range, deliver last page of results.
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
                template_object_name:story}
    if extra_context:
        context.update(extra_context)
    return render_to_response(template_name, context,
                            context_instance=RequestContext(request))
    