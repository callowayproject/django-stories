from django import forms
import datetime
from django.contrib.sites.models import Site

from models import Story

class StoryForm(forms.ModelForm):
    headline = forms.CharField(
        widget=forms.TextInput(attrs={'size':'85'}),
        max_length=100)
    subhead = forms.CharField(
        widget=forms.TextInput(attrs={'size':'85'}), 
        max_length=200, 
        required=False)
    tease_headline = forms.CharField(
        widget=forms.TextInput(attrs={'size':'85'}),
        max_length=100, required=False)
    kicker = forms.CharField(
        widget=forms.TextInput(attrs={'size':'85'}),
        max_length=50, required=False)
    
    non_staff_author = forms.CharField(
        widget=forms.TextInput(attrs={'size':'85'}),
        help_text="An HTML-formatted rendering of the author(s) not on staff.",
        max_length=200, 
        required=False)
    
    class Meta:
        model = Story
    
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                     initial=None, error_class=forms.util.ErrorList, label_suffix=':',
                     empty_permitted=False, instance=None):
        # Set a default publish time and the current site if it is a new object
        if not instance and (initial is not None and not initial.has_key('publish_date')):
            initial['publish_date'] = datetime.datetime.now().date()
        if not instance and (initial is not None and not initial.has_key('publish_time')):
            initial['publish_time'] = datetime.datetime.now().time().strftime('%H:%M:%S')
        if not instance and (initial is not None and not initial.has_key('site')):
            initial['site'] = Site.objects.get_current().id
        super(StoryForm, self).__init__(data, files, auto_id, prefix, initial, 
                                        error_class, label_suffix, 
                                        empty_permitted, instance)

    def clean_slug(self):
        if 'publish_date' in self.cleaned_data:
            publish_date = self.cleaned_data['publish_date']
            try:
                s = Story.objects.get(slug=self.cleaned_data['slug'],
                                      publish_date__year=publish_date.year,
                                      publish_date__month=publish_date.month,
                                      publish_date__day=publish_date.day)
                if s.id != self.instance.id:
                    raise forms.ValidationError(u"Please enter a different slug. The one you entered is already being used for %s" % publish_date.strftime("%Y-%m-%d"))
                else:
                    return self.cleaned_data['slug']
            except Story.DoesNotExist:
                pass
            else:
                raise forms.ValidationError(u"Please enter a different slug. The one you entered is already being used for %s" % publish_date.strftime("%Y-%m-%d"))
        return self.cleaned_data['slug']
