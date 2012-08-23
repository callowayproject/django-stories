from example.settings import *

INSTALLED_APPS += ('categories',)

import categories

from stories.models import Story
categories.register_fk(
    Story, 'primary_category', {'related_name': 'primary_category'})
categories.register_m2m(
    Story, 'categories', {'related_name': 'categories'})
