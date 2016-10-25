from django.db import models
from django.conf import settings
from member.models import MyUser


class Video(models.Model):
    kind = models.CharField(max_length=100)
    youtube_id = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    published_date = models.DateTimeField()
    registered_date = models.DateTimeField(auto_now_add=True)
    thumbnail = models.URLField(blank=True)
    users = models.ManyToManyField(MyUser)

    class Meta:
        ordering = ['-registered_date']

    def __str__(self):
        return self.title
