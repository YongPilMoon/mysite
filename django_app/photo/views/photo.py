from django.contrib import messages

from photo.models import Photo, PhotoLike, PhotoDisLike, Album
from django.shortcuts import get_object_or_404, redirect, render
from photo.form import MultiPhotoForm
__all__ = [
    'photo_like',
    'photo_delete',
    'photo_multi_add'
]

def photo_add(request):
    pass
    # if request.method == "POST":
    #     form = PhotoForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         title = form.cleaned_data['title']
    #         description = form.cleaned_data['description']
    #         img = form.cleaned_data['img']
    #         owner = request.user
    #         Photo.objects.create(
    #             album=album,
    #             owner=owner,
    #             title=title,
    #             description=description,
    #             img=img
    #         )
    #         messages.info(request, "새 앨범이 추가되었습니다.")
    #         return redirect('album:album_detail', album_pk=album_pk)


def photo_like(request, photo_pk, like_type='like'):
    photo = get_object_or_404(Photo, pk=photo_pk)
    album = photo.album
    next_path = request.GET.get('next')
    like_model = PhotoLike if like_type == 'like' else PhotoDisLike
    opposite_model = PhotoDisLike if like_type == 'like' else PhotoLike

    user_like_exist = like_model.objects.filter(
        user=request.user,
        photo=photo
    )

    if user_like_exist.exists():
        user_like_exist.delete()
    else:
        like_model.objects.create(
            user=request.user,
            photo=photo
        )

        opposite_model.objects.filter(
            user=request.user,
            photo=photo
        ).delete()

    if next_path:
        return redirect(next_path)
    else:
        return redirect('album:album_detail', album_pk=album.pk)


def photo_multi_add(request, album_pk):
    album = get_object_or_404(Album, pk=album_pk)
    if request.method == 'POST':
        form = MultiPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            files = request.FILES.getlist('img')
            for index, file in enumerate(files):
                Photo.objects.create(
                    album=album,
                    owner=request.user,
                    title= '%s(%s)' % (title, index),
                    description=description,
                    img=file,
                )
            return redirect('album:album_detail', album_pk=album_pk)
    else:
        form = MultiPhotoForm()
    context = {
        'form': form,
    }
    return render(request, 'album/photo_add.html', context)
































def photo_delete(request, photo_pk):
    photo = get_object_or_404(Photo,pk=photo_pk)
    album = photo.album
    photo.delete()
    return redirect('album:album_detail', album_pk=album.pk)