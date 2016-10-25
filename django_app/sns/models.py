from django.db import models


class FriendsRank(models.Model):
    friends_id = models.CharField(max_length=100)
    name = models.CharField(max_length=30)
    comment_count = models.IntegerField()
    picture_url = models.CharField(max_length=200)
