from django import template
from BeautifulSoup import BeautifulSoup

register = template.Library()

@register.filter
def add_attribute(tag, arg):
    """
    For paragraph pagination:

    {% for obj in paginator.object_list %}
        {% if forloop.first %}
        {{ obj|add_attribute:"class=dropcap" }}
        {% else %}
        {{ obj }}
        {% endif %}
    {% endfor %}
    """
    try:
        attr, val = arg.split('=')
        tag[attr] = val
    except Exception, e:
        pass
    return tag