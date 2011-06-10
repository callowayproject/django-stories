from django.contrib.admin.templatetags.admin_list import items_for_result, result_headers
from django.template import Library
from django.forms.models import modelform_factory

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
                    'fields':list(items_for_result(cl, res, form)), 
                    'quickedit':form,
                }
        else:
            for res, form in zip(cl.result_list, cl.formset.forms):
                yield list(items_for_result(cl, res, form))
    else:
        if qe_form:
            for res in cl.result_list:
                yield {'fields':list(items_for_result(cl, res, None)),}
        else:
            for res in cl.result_list:
                yield list(items_for_result(cl, res, None))

def qe_result_list(context, cl):
    if context.has_key('STATIC_URL'):
        static_url = 'STATIC_URL'
    else:
        static_url = 'MEDIA_URL'
    return {'cl': cl,
            'result_headers': list(result_headers(cl)),
            'results': list(results(cl)),
            'STATIC_URL': context[static_url]}
qe_result_list = register.inclusion_tag("admin/qe_change_list_results.html", takes_context=True)(qe_result_list)
