#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.template import (TemplateSyntaxError, Library,
                             Node, Variable, VariableDoesNotExist)

register = Library()

class RelatedNode(Node):
    """
    Main related object node that handles multiple template tags:

    * **get_related_content**
    * **get_related_content_type**
    * **get_relation_type**

    """
    def __init__(self, obj, var_name, content_type=None,
                 relation_type=None):

        self.content_type = content_type
        self.relation_type = relation_type
        self.obj = Variable(obj)
        self.var_name = var_name

    def render(self, context):
        try:
            obj = self.obj.resolve(context)
        except VariableDoesNotExist:
            return ''

        if self.content_type:
            items = obj.get_related_content_type(self.content_type)
        elif self.relation_type:
            items = obj.get_relation_type(self.relation_type)
        else:
            items = obj.storyrelation_set.all()

        context[self.var_name] = items
        return ''


@register.tag('get_related_content')
def do_get_related_content(parser, token):
    """
    Gets all relations to a story

    **Syntax**::

        {% get_related_content item as var_name %}

    **Example**::

        {% get_related_content story as story_rels %}

    """
    try:
        tag_name, obj, as_txt, var = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError(
            '"{0}" requires an object and a variable name.'.format(
                tag_name))

    return RelatedNode(obj, var)

@register.tag('get_related_content_type')
def do_get_related_content_type(parser, token):
    """
    Gets relations to a story based on the content type

    **Syntax**::

        {% get_related_content_type item content_type as var_name %}

    **Example**::

        {% get_related_content_type story Image as story_photos %}
    """
    try:
        tag_name, obj, content_type, as_txt, var = token.split_contents()
        content_type = content_type.replace("'", '').replace('"', '')
    except ValueError:
        raise TemplateSyntaxError(
            '"{0}" requires an object, content_type and a '\
            'variable name.'.format(tag_name))

    return RelatedNode(obj, var, content_type=content_type)

@register.tag('get_relation_type')
def do_get_relation_type(parser, token):
    """
    Gets the relations to a story based on the relation type

    **Syntax**::

        {% get_relation_type item relation_type as var_name %}

    **Example**::

        {% get_relation_type story leadphoto as leadphoto %}
    """
    try:
        tag_name, obj, relation_type, as_txt, var = token.split_contents()
        relation_type = relation_type.replace("'", '').replace('"', '')
    except ValueError:
        raise TemplateSyntaxError(
            '"{0}" requires an object, relation_type '\
            'and a variable name.'.format(tag_name))

    return RelatedNode(obj, var, relation_type=relation_type)

