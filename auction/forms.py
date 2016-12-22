from django.forms import ModelForm
from  django.forms import ChoiceField
from multiupload.fields import MultiFileField
from callboard.models import Category,SubCategory
from PIL import Image
from haystack.forms import SearchForm

from django import forms


class AuctionFilterForm(forms.Form):

    cat_obj = Category.objects.all()
    subcat_obj = SubCategory.objects.all()

    name = forms.CharField(label='Поиск',required=False, widget=forms.TextInput(attrs={'id':'auct_search'}))
    category = forms.ModelChoiceField(
                label='Категория',
                queryset=cat_obj,
                widget=forms.Select,
                required=False,
                empty_label='Все'
    )


    subcategory = forms.ModelChoiceField(
                label='Подкатегория',
                queryset=subcat_obj, #may be something like SubCategory.objects.filter(??????)
                widget=forms.Select,
                required=False,
                empty_label='Все')

    def __init__(self,*args, **kwargs):

        super(AuctionFilterForm, self ).__init__(*args, **kwargs)
        rec = kwargs.pop('data')

        if rec :
             print(rec)

             try:

                 val_cat = rec['category']
                 val_subcat = rec['subcategory']
             except:
                 val_cat = None
                 val_subcat = None

             if val_cat:
              self.fields['category'].initial =  rec['category']
              self.fields['subcategory'].queryset =  self.subcat_obj.filter(category_id=rec['category']).order_by('pk')
             if val_subcat:
                 self.fields['subcategory'].initial =   self.subcat_obj.filter(category_id=rec['category']).order_by('pk')
                 self.fields['subcategory'].initial =  rec['subcategory']



    #
    # min_price = forms.DecimalField(decimal_places=2,max_digits=10,required=False)
    # max_price = forms.DecimalField(decimal_places=2,max_digits=10,required=False)