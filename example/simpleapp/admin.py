from django.contrib import admin
from .models import BasicThing, BasicPhoto, BasicVideo, BasicAuthor

admin.site.register(BasicThing)
admin.site.register(BasicPhoto)
admin.site.register(BasicVideo)
admin.site.register(BasicAuthor)
