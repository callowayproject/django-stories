from django.conf.urls.defaults import *
from models import Profile

urlpatterns = patterns('',
    url(
        regex=r"^(?P<object_id>\d+)/?$",
        view="django.views.generic.list_detail.object_detail",
        kwargs={'queryset':Profile.objects.all()},
        name="profile_detail",
    ),
)