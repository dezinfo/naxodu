from django.forms import ModelForm
from  django.forms import ChoiceField
from multiupload.fields import MultiFileField
from advdesk.models import Goods, GoodsImageGallery


class AdverForm(ModelForm):

    files = MultiFileField(max_num=10, max_file_size=4024*4024*5,required=False)

    class Meta:
     model = Goods
     fields = ('category','subcategory','name','price')
     # exclude = ['user','is_active','creation_date','is_sell']


    def save(self, commit=True):
        instance = super(AdverForm, self).save(commit)
        for each in self.cleaned_data['files']:
         GoodsImageGallery.objects.create(file=each, good=instance,user=instance.user)
        return instance