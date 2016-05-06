from django.utils import timezone
from haystack import indexes

from .models import Articles

class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.EdgeNgramField(model_attr='name')
    body = indexes.CharField(model_attr='body')
    content_type = indexes.CharField(default='articles')
    def get_model(self):
        return Articles

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(creation_date__lte=timezone.now())

    def get_updated_field(self):
        return "updated"