from django.core.paginator import Paginator
from BeautifulSoup import BeautifulSoup

class ParagraphPaginator(Paginator):
    """
    A paginator that takes HTML-formatted text, and returns lists of paragraphs.
    This allows articles to keep paragraphs together. Working with some custom
    filters, it also allows for dynamically adding attributes to paragraph tags
    """
    
    def __init__(self, text, per_page, orphans=0, allow_empty_first_page=True):
        """
        Instead of an ``object_list`` this object takes an HTML-formatted string
        """
        soup = BeautifulSoup(text)
        self.object_list = soup.findAll('p')
        self.per_page = per_page
        self.orphans = orphans
        self.allow_empty_first_page = allow_empty_first_page
        self._num_pages = self._count = None


