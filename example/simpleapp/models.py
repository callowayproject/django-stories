from django.db import models
from django.db.models import permalink

class BasicThing(models.Model):
    """
    (BasicThing description)
    """

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'People'
        ordering = ('-created',)

    def __unicode__(self):
        return self.name

    @permalink
    def get_absolute_url(self):
        return ('basicthing_detail_view_name', [str(self.id)])

