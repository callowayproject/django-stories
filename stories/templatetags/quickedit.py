from django.contrib.admin.templatetags.admin_list import (items_for_result,
     result_headers, result_hidden_fields)
from django.template import Library

register = Library()


def results(cl):
    if hasattr(cl.model_admin, 'quick_editable'):
        qe_form = True
    else:
        qe_form = False
    if cl.formset:
        if qe_form:
            for res, form in zip(cl.result_list, cl.formset.forms):
                yield {
                    'fields': list(items_for_result(cl, res, form)),
                    'quickedit': form,
                }
        else:
            for res, form in zip(cl.result_list, cl.formset.forms):
                yield list(items_for_result(cl, res, form))
    else:
        if qe_form:
            for res in cl.result_list:
                yield {
                    'fields': list(items_for_result(cl, res, None)),
                }
        else:
            for res in cl.result_list:
                yield list(items_for_result(cl, res, None))


@register.inclusion_tag("admin/qe_change_list_results.html", takes_context=True)
def qe_result_list(context, cl):
    from django.conf import settings
    return {'cl': cl,
            'result_hidden_fields': list(result_hidden_fields(cl)),
            'result_headers': list(result_headers(cl)),
            'results': list(results(cl)),
            'STATIC_URL': context['STATIC_URL']}
qe_result_list = register.inclusion_tag(
    'admin/qe_change_list_results.html', takes_context=True)(qe_result_list)
