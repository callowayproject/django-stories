from django.db import models
from django.contrib.auth.models import User
from django.db.models import permalink

class Profile(models.Model):
    """
    (Profile description)
    """
    user = models.ForeignKey(User)
    name = models.CharField(blank=True, null=True, max_length=255)

    def __unicode__(self):
        return self.name

    @permalink
    def get_absolute_url(self):
        return ('profile_detail', (), {'object_id': self.id})

