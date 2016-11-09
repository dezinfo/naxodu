from django.forms import ModelForm
from  django.forms import ChoiceField
from multiupload.fields import MultiFileField
from callboard.models import Category,SubCategory
from PIL import Image
from haystack.forms import SearchForm

from django import forms


class AuctionFilterForm(forms.Form):
    name = forms.CharField(label='Поиск',required=False)
    category = forms.ModelChoiceField(
        label='Категория',
        queryset=Category.objects.all(),
        widget=forms.Select,
        required=False)

    subcategory = forms.ModelChoiceField(
        label='Подкатегория',
        queryset=SubCategory.objects.all(), #may be something like SubCategory.objects.filter(??????)
        widget=forms.Select,
        required=False)
    #
    # min_price = forms.DecimalField(decimal_places=2,max_digits=10,required=False)
    # max_price = forms.DecimalField(decimal_places=2,max_digits=10,required=False)