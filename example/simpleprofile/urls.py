from django.conf.urls.defaults import patterns, url
from .models import Profile

urlpatterns = patterns('',
    url(
        regex=r"^(?P<object_id>\d+)/?$",
        view="django.views.generic.list.ListView",
        kwargs={'queryset': Profile.objects.all()},
        name="profile_detail",
    ),
)
