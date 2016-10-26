from django.contrib import messages

from photo.models import Photo, PhotoLike, PhotoDisLike
from django.shortcuts import get_object_or_404, redirect

__all__ = [
    'photo_like',
    'photo_dislike'
]


def photo_like(request, photo_pk):
    photo = get_object_or_404(Photo, pk=photo_pk)
    album = photo.album
    user = request.user
    if PhotoLike.objects.filter(photo=photo, user=user).exists() or \
        PhotoDisLike.objects.filter(photo=photo, user=user).exists():
            messages.error(request, "이미 좋아요를 누르셨습니다.")
            return redirect('album:album_detail', album_pk=album.pk)

    PhotoLike.objects.create(
        photo=photo,
        user=user
    )

    return redirect('album:album_detail', album_pk=album.pk)


def photo_dislike(request, photo_pk):
    photo = get_object_or_404(Photo, pk=photo_pk)
    album = photo.album
    user = request.user
    if PhotoLike.objects.filter(photo=photo, user=user).exists() or \
            PhotoDisLike.objects.filter(photo=photo, user=user).exists():
        messages.error(request, "이미 좋아요를 누르셨습니다.")
        return redirect('album:album_detail', album_pk=album.pk)

    PhotoDisLike.objects.create(
        photo=photo,
        user=user
    )
    return redirect('album:album_detail', album_pk=album.pk)
