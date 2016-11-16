from django.forms import ModelForm
from  django.forms import ChoiceField
from multiupload.fields import MultiFileField
from callboard.models import Goods, GoodsImageGallery,Category,SubCategory,AttributeValue, AttributeMap
from PIL import Image
from haystack.forms import SearchForm
from tinymce.widgets import TinyMCE
from django import forms



class AdverForm(forms.ModelForm):


    # description = forms.CharField(widget=TinyMCE(attrs={'cols': 20, 'rows': 20}))



    class Meta:
     model = Goods
     fields = ('category','subcategory','name','description','price')
     # exclude = ['user','is_active','creation_date','is_sell']




    files = MultiFileField(max_num=10, max_file_size=4024*4024*5,required=False, label='Фото')

    def save(self, commit=True):
        instance = super(AdverForm, self).save(commit)
        for each in self.cleaned_data['files']:
            GoodsImageGallery.objects.create(file=each, good=instance, user = instance.user)






        return instance


class AddAttrForm(forms.Form):






    def __init__(self, *args, **kwargs):

        subcategory = kwargs.pop('sub_category')
        creation_flag = kwargs.pop('it_creation')



        super(AddAttrForm, self).__init__(*args, **kwargs)

        if  creation_flag!='yes':
             self.fields['q']  = forms.CharField(label='Поиск',required=False)


        list = subcategory.attributes.all().order_by('ordering')

        print(list)
        for i in list:
            if i.type == 'choice':

                self.fields[i] = forms.ModelChoiceField(
                            label=i.verbos_name,

                            queryset=AttributeValue.objects.filter(attribute=i),
                            widget=forms.Select(attrs={'class': i}),
                            required=i.required

                            )
            elif i.type == 'text':


                self.fields[i] = forms.CharField(
                            label=i.verbos_name,
                            required=i.required,
                            widget=forms.TextInput(attrs={'class': i})
                            )

            else:
                self.fields[i] = forms.IntegerField(
                            label=i.verbos_name,
                            required=i.required,
                            widget=forms.NumberInput(attrs={'class': i, 'min':"0"})
                            )

class GoodsSearchForm(SearchForm):

    def no_query_found(self):
        return self.searchqueryset.all()

CHOICE = []

class ProductFilterForm(forms.Form):
    q = forms.CharField(label='Поиск',required=False)
    category = forms.ModelChoiceField(
        label='Категория',
        queryset=Category.objects.all(),
        widget=forms.Select,
        required=False)

    subcategory = forms.ModelChoiceField(
        label='Категория',
        queryset=SubCategory.objects.all(), #may be something like SubCategory.objects.filter(??????)
        widget=forms.Select,
        required=False)

    min_price = forms.DecimalField(decimal_places=2,max_digits=10,required=False)
    max_price = forms.DecimalField(decimal_places=2,max_digits=10,required=False)


