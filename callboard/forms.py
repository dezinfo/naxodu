from django.forms import ModelForm
from  django.forms import ChoiceField
from multiupload.fields import MultiFileField
from callboard.models import Goods, GoodsImageGallery,Category,SubCategory,AttributeValue, AttributeMap
from PIL import Image
from haystack.forms import SearchForm
from tinymce.widgets import TinyMCE
from django import forms
from userprofile.models import UserProfileTable



class EditAdvertForm(forms.ModelForm):

  class Meta:
     model = Goods
     fields = ('name','description','price')


class EditAttrForm(forms.Form):

    

    def __init__(self, *args, **kwargs):
         
         obj = kwargs.pop('obj')
         # att_map = AttributeMap.objects.filter(product_name=obj).order_by('attribute_name__ordering')
         # g = Goods.objects.get(pk=obj.pk)
         att_map = obj.subcategory.attributes.all().order_by('ordering')
         attributes = obj.attributes
         print(att_map)

         super(EditAttrForm, self).__init__(*args, **kwargs)

         for i in att_map:

             try:
                initial = attributes[i.name]['value']
             except:
                 initial = ''

             if i.type == 'choice':

                    self.fields[i.name] = forms.ModelChoiceField(
                                label=i.verbos_name,
                                initial=initial,

                                queryset=AttributeValue.objects.filter(attribute=i),
                                widget=forms.Select(attrs={'class': i.name, 'name':i.name},),
                                required=i.required


                                )

             elif i.type == 'text':


                    self.fields[i.name] = forms.CharField(
                                label=i.verbos_name,
                                initial=initial,
                                required=i.required,
                                widget=forms.TextInput(attrs={'class': i.name,'name':i.name})
                                )
                    # print(i.attribute_value_manual)
             else:
                    self.fields[i.name] = forms.IntegerField(
                                label=i.verbos_name,
                                initial=initial,
                                required=i.required,
                                widget=forms.NumberInput(attrs={'class': i.name, 'min':"0",'name':i.name})
                                )
                    # print(i.attribute_value_manual)



class AdverForm(forms.ModelForm):




    # def __init__(self, *args, **kwargs):
    #
    #     user = kwargs.pop('user')
    #     super(AdverForm, self).__init__(*args, **kwargs)
    #     print(user.userprofiletable_set.get().adress_state)
    #
    #     state = user.userprofiletable_set.get().adress_state
    #     city = user.userprofiletable_set.get().adress_city
    #
    #
    #     if state and city:
    #         self.fields['state'].initial = state
    #         self.fields['city'].initial = city


    class Meta:
     model = Goods
     fields = ('category','subcategory','types','name','description','price',

               'state','city'
               )
     # exclude = ['user','is_active','creation_date','is_sell']




    files = MultiFileField(max_num=10, max_file_size=4024*4024*5,required=False, label='Фото')

    def save(self, commit=True):
        instance = super(AdverForm, self).save(commit)
        for each in self.cleaned_data['files']:
            GoodsImageGallery.objects.create(file=each, good=instance, user = instance.user)






        return instance







class AddAttrFilterForm(forms.Form):


    q  = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Поиск'}))

    def __init__(self, *args, **kwargs):

        subcategory = kwargs.pop('sub_category')



        super(AddAttrFilterForm, self).__init__(*args, **kwargs)




        list = subcategory.attributes.filter(filtering=True).order_by('ordering')

        # print(list)
        for i in list:
            if i.attr_type == 'choice':

                self.fields[i] = forms.ModelChoiceField(
                            label=i.verbos_name,

                            queryset=AttributeValue.objects.filter(attribute=i),
                            widget=forms.Select(attrs={'class': i}),
                            empty_label= i.verbos_name,

                            required=False

                            )
            elif i.attr_type == 'text':


                self.fields[i] = forms.CharField(
                            label=i.verbos_name,
                            required=False,
                            widget=forms.TextInput(attrs={'class': i,'placeholder':i.verbos_name})
                            )

            else:
                self.fields[i] = forms.IntegerField(
                            label=i.verbos_name,
                            required=False,
                            widget=forms.NumberInput(attrs={'class': i, 'min':"0", 'placeholder':i.verbos_name})
                            )






class AddAttrForm(forms.Form):

    def __init__(self, *args, **kwargs):

        subcategory = kwargs.pop('sub_category')
        type = kwargs.pop('type_id')
        # creation_flag = kwargs.pop('it_creation')



        super(AddAttrForm, self).__init__(*args, **kwargs)
        if type:
            list = type.attributes.all().order_by('ordering')
        else:
            list = subcategory.attributes.all().order_by('ordering')

        # print(list)
        for i in list:
            if i.attr_type == 'choice':

                self.fields[i] = forms.ModelChoiceField(
                            label=i.verbos_name,

                            queryset=AttributeValue.objects.filter(attribute=i),
                            widget=forms.Select(attrs={'class': i}),
                            required=i.required

                            )
            elif i.attr_type == 'text':


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


