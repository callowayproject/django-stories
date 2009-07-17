# Create your views here.
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.conf import settings
from django.shortcuts import get_object_or_404, render_to_response

from stories.models import ChangeSet, Story
from django.contrib.admin.views.decorators import staff_member_required

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
    