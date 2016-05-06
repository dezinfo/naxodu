from django.utils import timezone
from haystack import indexes

from .models import Goods

class GoodIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    auto_name = indexes.EdgeNgramField(model_attr='name')
    description = indexes.CharField(model_attr='description')
    content_type = indexes.CharField(default='goods')
    is_active = indexes.CharField(model_attr='is_active')

    def get_model(self):
        return Goods


    def get_updated_field(self):
        return "updated"

