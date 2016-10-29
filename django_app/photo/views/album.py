from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from photo.models import Album, Photo
from photo.form import AlbumForm, PhotoForm

__all__ = [
    "album_list",
    "album_detail",
    "album_edit",
    "album_add",
]


@login_required
def album_list(request):
    albums = Album.objects.all()
    form = AlbumForm
    context = {
        "albums": albums,
        "form": form,
        }
    return render(request, 'album/album_list.html', context)


@login_required
def album_detail(request, album_pk):
    album = get_object_or_404(Album, pk=album_pk)
    context = {
        'album': album
    }

    return render(request, 'album/ajax_album_detail.html', context)


def album_edit(request, album_pk):
    album = get_object_or_404(Album, pk=album_pk)
    if request.method == "POST":
        form = AlbumForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            owner = request.user
            Album.objects.filter(pk=album.pk).update(
                title=title,
                description=description,
                owner=owner
            )
            messages.info(request, "앨범이 수정되었습니다.")
            return redirect('album:album_list')
    else:
        default_data = {
            'title': album.title,
            'description': album.description
        }
        form = AlbumForm(default_data)

        context = {
            "form": form,
        }
        return render(request, 'album/album_edit.html', context)


def album_add(request):
    if request.method == "POST":
        form = AlbumForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            owner = request.user
            Album.objects.create(
                title=title,
                description=description,
                owner=owner
            )
            messages.info(request, "새 앨범이 추가되었습니다.")
            return redirect('album:album_list')

