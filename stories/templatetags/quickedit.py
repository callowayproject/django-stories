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
                yield {'fields':list(items_for_result(cl, res, form)), 
                'quickedit':form}
                #'quickedit':form(instance=res)}
        else:
            for res, form in zip(cl.result_list, cl.formset.forms):
                yield list(items_for_result(cl, res, form))
    else:
        if qe_form:
            for res in cl.result_list:
                yield {'fields':list(items_for_result(cl, res, None)), 
                'quickedit':form}
                #'quickedit':form(instance=res)}
        else:
            for res in cl.result_list:
                yield list(items_for_result(cl, res, None))

def qe_result_list(cl):
    return {'cl': cl,
            'result_headers': list(result_headers(cl)),
            'results': list(results(cl)),}
qe_result_list = register.inclusion_tag("admin/qe_change_list_results.html")(qe_result_list)
