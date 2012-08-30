#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module

def load_widget(path):
    """Utily to import a custom widget module"""

    if not path:
        return

    index = path.rfind('.')
    module, attr = path[:index], path[index + 1:]

    try:
        mod = import_module(module)
        return getattr(mod, attr)
    except (ImportError, ValueError, AttributeError), e:
        raise ImproperlyConfigured(
            'Error importing widget {0}: "{1}"'.format(path, e))
