from django.forms import ModelForm
from community.models import Articles, Forums

class NewArticleForm(ModelForm):






    class Meta:
     model = Articles
     fields = ('name','body')
     # exclude = ['user','is_active','creation_date','is_sell']


class CreateForum(ModelForm):

    class Meta:
        model = Forums
        fields = ('name','description','image')