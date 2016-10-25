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
    # Myuser가 Photo를 참조 할때 필요한 이름을 명시해 준다.
    like_users = models.ManyToManyField(MyUser, through='PhotoLike', related_name='photo_set_like_users')
    dislike_users = models.ManyToManyField(MyUser, through='PhotoDisLike', related_name='photo_set_dislike_users')


class PhotoLike(models.Model):
    photo = models.ForeignKey(Photo)
    user = models.ForeignKey(MyUser)
    created_date = models.DateTimeField(auto_now_add=True)


class PhotoDisLike(models.Model):
    photo = models.ForeignKey(Photo)
    user = models.ForeignKey(MyUser)
    created_date = models.DateTimeField(auto_now_add=True)
