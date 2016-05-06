from django.forms import ModelForm
from  django.forms import ChoiceField
from multiupload.fields import MultiFileField
from callboard.models import Goods, GoodsImageGallery
from PIL import Image
from haystack.forms import SearchForm
from tinymce.widgets import TinyMCE
from django import forms



class AdverForm(ModelForm):


    description = forms.CharField(widget=TinyMCE(attrs={'cols': 20, 'rows': 30}))



    class Meta:
     model = Goods
     fields = ('category','subcategory','subtype','name','description','condition','price')
     # exclude = ['user','is_active','creation_date','is_sell']


    files = MultiFileField(max_num=10, max_file_size=4024*4024*5,required=False)

    def save(self, commit=True):
        instance = super(AdverForm, self).save(commit)
        for each in self.cleaned_data['files']:
            GoodsImageGallery.objects.create(file=each, good=instance, user = instance.user)

        return instance





class GoodsSearchForm(SearchForm):

    def no_query_found(self):
        return self.searchqueryset.all()