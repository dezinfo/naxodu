from django.db import models
from django.db.models.signals import post_save
from django.conf import settings

from community.models import Forums
from django.contrib.auth.models import User
from smart_selects.db_fields import ChainedForeignKey

MAIL_STATUS = (('Unread','Не прочитано'),('Readed','Прочитано'))

# Create your models here.

class States(models.Model):
    state = models.CharField(max_length=100)

    def __str__(self):              # __unicode__ on Python 2
        return str(self.state)

class Cities(models.Model):
    state = models.ForeignKey(States)
    city = models.CharField(max_length=120)

    def __str__(self):              # __unicode__ on Python 2
        return str(self.city)

class UserProfile(models.Model):
    username = models.ForeignKey(User,blank=True, on_delete=models.CASCADE)
    favorites = models.ManyToManyField(User, related_name='favorited_by_user',blank=True)
    user_image = models.ImageField(verbose_name='Аватар',blank=True,default=settings.STATIC_URL+'images/avatar.jpeg')
    adress_state = models.ForeignKey(States,verbose_name='Область',null=True,blank=True)
    adress_city =  ChainedForeignKey(
        Cities,
        chained_field="state",
        chained_model_field="state",
        show_all=False,
        auto_choose=True, verbose_name='Город',blank=True
        )
    discount_percent = models.IntegerField(verbose_name='Процент скидки',default=5)
    phone = models.IntegerField(verbose_name='Телефон',blank=True,null=True)
    skype = models.CharField(max_length=100,verbose_name='Скайп',blank=True,null=True)

    def __str__(self):              # __unicode__ on Python 2
        return str(self.username)


def create_user_profile(sender, instance, created, **kwargs):

    if created:

        UserProfile.objects.create(username=instance)



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