from django.contrib import admin
from .models import Album, Photo, PhotoDisLike, PhotoLike

# Register your models here.
admin.site.register(Album)
admin.site.register(Photo)
admin.site.register(PhotoLike)
admin.site.register(PhotoDisLike)