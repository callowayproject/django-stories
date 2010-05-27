from django.core.management.base import BaseCommand
from django.core.exceptions import ImproperlyConfigured
from stories.models import Story

import datetime, time
from HTMLParser import HTMLParseError

try:
    from tidylib import tidy_fragment
except ImportError:
    raise ImproperlyConfigured('You must install pytidylib')
try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    raise ImproperlyConfigured('You must install BeautifulSoup')


class Command(BaseCommand):
    args = '<url> [<url>]'
    help = 'Validates the story at the given URL for valid HTML, and attempts to correct it if invalid.'
    
    def handle(self, *args, **kwargs):
        month_format='%b'
        day_format='%d'
        for url in args:
            parts = url.split('/')
            
            if len(parts) < 4:
                return "URL doesn't parse into at least year/month/day/slug"
            if parts[-1] == "":
                empty = parts.pop()
            slug = parts.pop()
            day = parts.pop()
            month = parts.pop()
            year = parts.pop()
            try:
                tt = time.strptime('%s-%s-%s' % (year, month, day),
                                   '%s-%s-%s' % ('%Y', month_format, day_format))
                date = datetime.date(*tt[:3])
            except ValueError:
                raise Http404
            story = Story.objects.get(publish_date=date, slug=slug)
            try:
                BeautifulSoup(story.body) # error that happens in paginator
                print "Story HTML is valid."
            except HTMLParseError, e:
                story.body = tidy_fragment(story.body)[0] # tidy the frag
                print "Story HTML is invalid, fixing and saving story."
                story.save()
                try:
                    BeautifulSoup(story.body) # error that happens in paginator
                    print "Story HTML is valid."
                except HTMLParseError, e:
                    print "Story HTML was not able to be fixed. Object pk: %s" % story.id
            