from operator import mod
from statistics import mode
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


User._meta.get_field('username')._unique = True
User._meta.get_field('email')._unique = True


class Picture(models.Model):
    user_pk = models.CharField(default="",max_length= 40)
    image = models.CharField(default='default.png',max_length=300)
    size = models.CharField(default= "", max_length = 30)
    comment = models.TextField(default="")
    artist_id = ArrayField(models.CharField(blank=True,max_length=300), default=list)
    match = models.IntegerField(default=0)



class CustomUser(AbstractBaseUser):
    email = models.EmailField(_('email address'), unique=True)
    password = models.CharField(_('password'),  max_length=220)
    first_name = models.CharField(_('first_name'),  max_length=20)
    last_name = models.CharField(_('last_name'),  max_length=30)
    username = models.CharField(_('username'),  max_length=30)
    date_joined = models.DateTimeField(default=timezone.now)
    user_type = models.CharField(default="", max_length=12)
    profile_image = models.CharField(default='default.png',max_length=300)
    
    USERNAME_FIELD = 'email'
    
    
class MatchRelationship(models.Model):
    user_pk = models.CharField(default="",max_length= 40)
    artist = models.CharField(default="",max_length= 40)
    picture_pk = models.ForeignKey(Picture,on_delete=models.CASCADE, default="")