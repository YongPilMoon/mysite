import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from photo.models import Photo, PhotoLike, PhotoDisLike

__all__ = [
    'ajax_photo_like',
]


@require_POST
@csrf_exempt
def ajax_photo_like(request, photo_pk, like_type='like'):
    photo = get_object_or_404(Photo, pk=photo_pk)
    album = photo.album
    next_path = request.GET.get('next')
    like_model = PhotoLike if like_type == 'like' else PhotoDisLike
    opposite_model = PhotoDisLike if like_type == 'like' else PhotoLike

    user_like_exist = like_model.objects.filter(
        user=request.user,
        photo=photo
    )

    is_delete = False
    if user_like_exist.exists():
        user_like_exist.delete()
        is_delete = True
    else:
        like_model.objects.create(
            user=request.user,
            photo=photo
        )

        opposite_model.objects.filter(
            user=request.user,
            photo=photo
        ).delete()
    ret = {
        'like_count': photo.like_users.count(),
        'dislike_count': photo.dislike_users.count(),
        'user_like': False,
        'user_dislike': False,
        # 'user_like': True if photo.like_users.filter(pk=request.user.pk).exists() else False,
        # 'user_dislike': True if photo.dislike_users.filter(pk=request.user.pk).exists() else False,
    }
    if not is_delete:
        ret['user_like'] = True if like_type == 'like' else False
        ret['user_dislike'] = True if like_type != 'like' else False

    #dumps dic을 json으로 바꾼다.
    return HttpResponse(json.dumps(ret), content_type='application/json')