import os

from django.db import models
from member.models import MyUser
from mysite.utils.models import BaseModel


class Album(BaseModel):
    title = models.CharField(max_length=40)
    owner = models.ForeignKey(MyUser)
    description = models.CharField(max_length=80, blank=True)

    def __str__(self):
        return self.title


class Photo(BaseModel):
    album = models.ForeignKey(Album)
    owner = models.ForeignKey(MyUser)
    title = models.CharField(max_length=40)
    description = models.CharField(max_length=80, blank=True)
    # 업로드 폴더를 Photo로 지정한다.
    img = models.ImageField(upload_to='photo')
    img_thumbnail = models.ImageField(upload_to='photo/thumbnail', blank=True)
    # Myuser가 Photo를 참조 할때 필요한 이름을 명시해 준다.
    like_users = models.ManyToManyField(MyUser, through='PhotoLike', related_name='photo_set_like_users', default=0)
    dislike_users = models.ManyToManyField(MyUser, through='PhotoDisLike', related_name='photo_set_dislike_users', default=0)

    def delete(self, *args, **kwargs):
        os.remove(self.img.path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.title

    def url_thumbnail(self):
        return self.url_field('img_thumbnail', default='/static/img/default.jpg')

    def make_thumbnail(self):
        import os
        from PIL import Image, ImageOps
        from io import BytesIO
        from django.core.files.base import ContentFile
        from django.core.files.storage import default_storage
        size = (300, 300)
        f = default_storage.open(self.img)

        image = Image.open(f)
        ftype = image.format

        image = ImageOps.fit(image, size, Image.ANTIALIAS)

        path, ext = os.path.splitext(self.img.name)
        name = os.path.basename(path)

        thumbnail_name = '%s_thumb%s' % (name, ext)

        temp_file = BytesIO()
        image.save(temp_file, ftype)
        temp_file.seek(0)

        content_file = ContentFile(temp_file.read())
        self.img_thumbnail.save(thumbnail_name, content_file)

        temp_file.close()
        content_file.close()
        f.close()

    def save(self, *args, **kwargs):
            image_changed = False

            if self.img and not self.img_thumbnail:
                image_changed = True

            if self.pk:
                ori = Photo.objects.get(pk=self.pk)
                if ori.img != self.img:
                    image_changed = True

            super().save(*args, **kwargs)
            if image_changed:
                self.make_thumbnail()


class PhotoLike(BaseModel):
    photo = models.ForeignKey(Photo)
    user = models.ForeignKey(MyUser)
    created_date = models.DateTimeField(auto_now_add=True)


class PhotoDisLike(BaseModel):
    photo = models.ForeignKey(Photo)
    user = models.ForeignKey(MyUser)
    created_date = models.DateTimeField(auto_now_add=True)
