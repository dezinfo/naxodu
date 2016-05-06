from django.contrib.auth.models import User
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from pytils.translit import slugify
import itertools

# Create your models here.


def get_upload_file_name(instance, filename):
    return 'uploaded_files/%s/%s' % (instance.name,filename)

class Forums(models.Model):
    name = models.CharField(verbose_name='Имя форума',blank=False,max_length=70,unique=True)
    description = models.TextField(verbose_name='Краткое описание',blank=True,max_length=1000)
    creation_date = models.DateTimeField(verbose_name='date published',auto_now_add=True)
    username = models.ForeignKey(User,max_length=100,verbose_name='Пользователь')
    image = models.ImageField(verbose_name='Изображение', upload_to=get_upload_file_name,blank=True)
    slug = models.SlugField(max_length=70,unique=True)
    follow = models.ManyToManyField(User,blank=True,related_name='forums_follow')
    official_status = models.BooleanField(default=True)

    def __str__(self):              # __unicode__ on Python 2
        return self.name

    class Meta:
        managed=True

    def get_last_article(self):
        return self.articles_set.filter().latest('creation_date')

    def save(self,*args,**kwargs):


        self.slug = slugify(self.name)
        super(Forums, self).save(*args, **kwargs)

class Articles(models.Model):
    forum = models.ForeignKey(Forums,verbose_name='Форум')
    name = models.CharField(max_length=200,verbose_name='Заголовок')
    body = RichTextUploadingField(verbose_name='Описание')
    username = models.ForeignKey(User)
    creation_date = models.DateTimeField(verbose_name='date published',auto_now_add=True)
    slug = models.SlugField(max_length=70,unique=True,blank=True)
    follow = models.ManyToManyField(User,blank=True,related_name='articles_follow')
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    def __str__(self):              # __unicode__ on Python 2
        return self.name

    class Meta:
        managed=True


    def save(self,*args,**kwargs):

        if not self.slug:
            # self.slug = slugify(self.name)
            self.slug = orig = slugify(self.name)

            for x in itertools.count(1):
                if not Articles.objects.filter(slug=self.slug).exists():
                    break
                self.slug = '%s-%d' % (orig, x)

        super(Articles, self).save(*args, **kwargs)


    def forum_slug(self):
        return  self.forum.slug
