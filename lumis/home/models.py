from django.conf import settings
from django.db import models

full_path = 'H:\Lumis\lumis\sources\\'

class Link(models.Model):
    url = models.CharField(max_length=200, primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, primary_key=True)
    createDate = models.DateTimeField(auto_now_add=True, blank=True)
    active = models.BooleanField()
    dateLast = models.DateTimeField(null=True)


class Photo(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True)
    #url = models.CharField(max_length=400)
    image = models.ImageField(upload_to=settings.MEDIA_ROOT)
    publishedDate = models.DateTimeField(auto_now_add=True, blank=True)


class Like(models.Model):
    photo = models.ForeignKey('Photo', related_name='authorPhoto', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)
