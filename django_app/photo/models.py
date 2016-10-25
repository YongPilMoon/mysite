from django.db import models
from member.models import MyUser


class Album(models.Model):
    title = models.CharField(max_length=40)
    owner = models.ForeignKey(MyUser)
    description = models.CharField(max_length=80, blank=True)


class Photo(models.Model):
    Album = models.ForeignKey(Album)
    owner = models.ForeignKey(MyUser)
    title = models.CharField(max_length=40)
    description = models.CharField(max_length=80, blank=True)
    img = models.ImageField(upload_to='photo')


