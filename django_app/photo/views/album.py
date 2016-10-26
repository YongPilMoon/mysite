from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from photo.models import Album, Photo
from photo.form import AlbumForm, PhotoForm

__all__ = [
    "album_list",
    "album_detail",
]


@login_required
def album_list(request):
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
    else:
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
    if request.method == "POST":
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            print("===============================")
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            img = form.cleaned_data['img']
            owner = request.user
            Photo.objects.create(
                album=album,
                owner=owner,
                title=title,
                description=description,
                img=img
            )
            messages.info(request, "새 앨범이 추가되었습니다.")
            return redirect('album:album_detail', album_pk=album_pk)
    else:
        photos = Photo.objects.filter(album=album)
        form = PhotoForm(request.POST)
        context = {
            "photos": photos,
            "form": form,
        }
        return render(request, 'album/album_detail.html', context)