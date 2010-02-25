from django.db import models

# Create your models here.
class BasicThing(models.Model):
    """
    (BasicThing description)
    """
    
    name        = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'People'
        ordering = ('-created',)
    
    def __unicode__(self):
        return self.name
    
    # If using the get_absolute_url method, put the following line at the top of this file:
    from django.db.models import permalink
    
    @permalink
    def get_absolute_url(self):
        return ('basicthing_detail_view_name', [str(self.id)])
    
