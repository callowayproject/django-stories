from django.http import HttpResponse

# Need this in the javascript:

class MarkupBase(object):
    """
    The base class for a markup language.
    """
    prefix = 'txt'
    gui_js = ''
    
    @classmethod
    def get_gui(request):
        """
        Return a JSON object to load the gui
        """
        return HttpResponse('{}', content_type="application/x-javascript")
    
    @classmethod
    def validate(content):
        """
        Validate the content. Typically called before saving the content.
        
        Return False if the content is not valid
        """
        return True
    
    @classmethod
    def to_html(content):
        """
        Convert the content to HTML
        """
        return content


class HTMLMarkup(MarkupBase):
    """
    Implementation of HMTL markup for a story
    """
    prefix = 'htm'
    js = ''
    
    @classmethod
    def get_gui(request):
        """
        Handle the AJAX request for the GUI markup
        """
        # Return javascript that inserts
        pass