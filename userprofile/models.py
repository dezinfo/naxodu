from PIL import Image
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.utils.timezone import now
from community.models import Forums
from django.contrib.auth.models import User
from smart_selects.db_fields import ChainedForeignKey

MAIL_STATUS = (('Unread','Не прочитано'),('Readed','Прочитано'))

# Create your models here.

def get_upload_file_name(instance, filename):
    return 'user_avatar/%s/%s' % (instance.username,instance.username+instance.file_extension)

class States(models.Model):
    state = models.CharField(max_length=100)

    def __str__(self):              # __unicode__ on Python 2
        return str(self.state)

class Cities(models.Model):
    state = models.ForeignKey(States)
    city = models.CharField(max_length=120)

    def __str__(self):              # __unicode__ on Python 2
        return str(self.city)

class UserProfileTable(models.Model):
    username = models.ForeignKey(User,blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20,verbose_name='Имя',blank=True,null=True)
    last_name = models.CharField(max_length=40,verbose_name='Фамилия',blank=True,null=True)
    favorites = models.ManyToManyField(User, related_name='favorited_by_user',blank=True)
    user_image = models.ImageField(verbose_name='Аватар',blank=True,default='avatar.jpeg', upload_to=get_upload_file_name)
    adress_state = models.ForeignKey(States,verbose_name='Область',blank=True,null=True,)
    adress_city =  ChainedForeignKey(
        Cities,
        chained_field="adress_state",
        chained_model_field="state",
        show_all=False,
        auto_choose=False, verbose_name='Город',blank=True,null=True
        )
    discount_percent = models.IntegerField(verbose_name='Процент скидки',default=5)
    phone = models.IntegerField(verbose_name='Телефон',blank=True,null=True)
    skype = models.CharField(max_length=100,verbose_name='Скайп',blank=True,null=True)
    last_visit = models.DateTimeField(verbose_name='Последнее посещение',blank=True, null=True)

    def __str__(self):              # __unicode__ on Python 2
        return str(self.username)


    def get_absolute_url(self):

        return  reverse('userprofile', kwargs={'username': self.username})

    def save(self,**kwargs):


        image = Image.open(self.user_image)
        if image.size[1] > 1200:
            basewidth = 1200
            percent = (basewidth / float(image.size[0]))
            hsize = int((float(image.size[1]) * float(percent)))
            image = image.resize((basewidth,hsize), Image.ANTIALIAS)
            image.save(self.user_image.path)

        super(UserProfileTable, self).save()

def create_user_profile(sender, instance, created, **kwargs):

    if created:

        UserProfileTable.objects.create(username=instance)



post_save.connect(create_user_profile, sender=User)


class Inbox(models.Model):
    to_user = models.ForeignKey(User)
    from_user = models.ForeignKey(User,related_name='sender')
    status = models.CharField(max_length=20,choices=MAIL_STATUS,blank=True)
    subject = models.CharField(max_length=300,blank=True)
    body = models.TextField(blank=True)
    creation_date = models.DateTimeField('date published',auto_now_add=True)
#



# Example how to get MtoM value
# up.favorites.values()[0].get('name')
# up.favorites.values()[0].get('name')