from example.settings import *

INSTALLED_APPS += ('categories',)

CATEGORIES_SETTINGS = {
    'FK_REGISTRY': {
        'stories.story': {
            'name': 'primary_category', 'related_name': 'primary_category'
        }
    },
    'M2M_REGISTRY': {
        'stories.story': {
            'name': 'categories', 'related_name': 'categories'
        }
    }
}

STORY_SETTINGS = {
    'ADMIN_EXTRAS': {
        'RAW_ID_FIELDS': ('primary_category',),
        'FILTER_HORIZONTAL_FIELDS': ('categories', 'authors',),
        'EXTRA_FIELDSETS': (
            {'name': 'Categories',
             'fields': ('primary_category', 'categories'),
             'position': 1
            },
        )
    }
}
