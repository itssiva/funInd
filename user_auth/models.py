from django.db import models
from django.contrib.auth.models import User
from django.conf import settings as django_settings
import os
from django.db.models.signals import post_save
from django.contrib import admin
# Create your models here.
# Create a profile model to store info about users

class Profile(models.Model):
    user = models.OneToOneField(User)
    url = models.CharField(max_length=100)

    class Meta:
        db_table = 'auth_profile'

    def get_url(self):
        url = self.url
        if "http://" not in self.url and "https://" not in self.url and len(self.url)>0:
            url = "http://" + str(self.url)
        return url

    def get_profile_pic(self):
        # If the user does not have a picture then a default pic is set as the profile_pic
        no_picture = django_settings.STATIC_URL + 'img/user.png'
        #Try to find if the user already has a picture
        try:
            filename = django_settings.MEDIA_ROOT + '/profile_pictures/'+self.user.username+'.jpg'
            picture_url  = django_settings.MEDIA_URL + 'profilepictures/'+self.user.username+'.jpg'
            if os.path.isfile(filename):
                return picture_url
            else:
                return no_picture
        except Exception :
            return no_picture

    def get_screen_name(self):
        try:
            if self.user.get_full_name():
                return self.user.get_full_name()
            else:
                self.user.username
        except:
            return self.user.username

class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user"]


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)

admin.site.register(Profile, ProfileAdmin)




