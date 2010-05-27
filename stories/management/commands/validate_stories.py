from django.core.management.base import BaseCommand
from django.core.exceptions import ImproperlyConfigured
from stories.models import Story

try:
    from tidylib import tidy_fragment
    from BeautifulSoup import BeautifulSoup, HTMLParseError
except ImportError:
    raise ImproperlyConfigured('You must install BeautifulSoup and pytidylib')


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for story in Story.objects.filter(status=4):
            try:
                BeautifulSoup(story.body)
            except HTMLParseError, e:
                story.body = tidy_fragment(story.body)
                story.save()