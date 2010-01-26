from django import template

register = template.Library()
@register.tag(name='dict_get')
def do_dict(parser, token):
    try:
        tag_name, dictname, key = token.contents.split(None, 2)
    except ValueError:
        raise template.TemplateSyntaxError("'dict_get' node requires a dict and a key name.")
    # nodelist = parser.parse(('enddict',))
    # parser.delete_first_token()
    return DictNode(dictname, key)

class DictNode(template.Node):
    def __init__(self, dictname, key):
        self.dictname = template.Variable(dictname)
        self.key = template.Variable(key)
        
    def render(self, context):
        try:
            the_dict = self.dictname.resolve(context)
            the_key = self.key.resolve(context)
            return the_dict.get(the_key, 'na')
        except template.VariableDoesNotExist:
            return ''


def reversion_submit_row(context):
    opts = context['opts']
    change = context['change']
    is_popup = context['is_popup']
    save_as = context['save_as']
    return {
        'onclick_attrib': (opts.get_ordered_objects() and change
                            and 'onclick="submitOrderForm();"' or ''),
        'show_delete_link': (not is_popup and context['has_delete_permission']
                              and (change or context['show_delete'])),
        'show_save_as_new': not is_popup and change and save_as,
        'show_save_and_add_another': context['has_add_permission'] and 
                            not is_popup and (not save_as or context['add']),
        'show_save_and_continue': not is_popup and context['has_change_permission'],
        'is_popup': is_popup,
        'show_save': True
    }
reversion_submit_row = register.inclusion_tag('admin/stories/submit_line.html', takes_context=True)(reversion_submit_row)
