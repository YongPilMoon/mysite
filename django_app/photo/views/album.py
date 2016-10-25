from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from photo.models import Album
from photo.form import AlbumForm

__all__ = [
    "album_list"
]

@login_required
def album_list(request):
    if request.method == "POST":
        form = AlbumForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']

            Album.objects.create(
                title=title,
                description=description,
                owner=request.user
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

