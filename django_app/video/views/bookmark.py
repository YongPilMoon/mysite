from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from video.models import Video
from django.contrib.auth.decorators import login_required

__all__ = [
    'bookmark_add',
    'bookmark_list',
    'bookmark_detail',
    'bookmark_delete',
]

@login_required
def bookmark_add(request):
    path = request.POST.get('path')
    try:
        kind = request.POST['kind']
        video_id = request.POST['video_id']
        title = request.POST['title']
        description = request.POST['description']
        published_date = request.POST['published_date']
        thumbnail_url = request.POST['thumbnail_url']
        user = request.user

        if Video.objects.filter(youtube_id=video_id).exists():
            video = Video.objects.get(youtube_id=video_id)
        else:
            video = Video.objects.create(
                kind=kind,
                youtube_id=video_id,
                title=title,
                description=description,
                published_date=published_date,
                thumbnail=thumbnail_url,
            )

        video.users.add(user)
        msg = '%s 영상을 북마크에 등록했습니다' % (
            video.title
        )
    except Exception as e:
        msg = 'Exception! %s (%s)' % (e, e.args)

    messages.success(request, msg)
    if path:
        return redirect(path)
    else:
        return redirect('video:bookmark_list')

@login_required
def bookmark_list(request):
    """
    추가한 Video인스턴스 목록을 보여주는 페이지
    """
    user = request.user
    videos = Video.objects.filter(users__pk=user.pk)
    context = {
        'videos': videos,
    }
    return render(request, 'video/bookmark_list.html', context)

@login_required
def bookmark_detail(request, pk):
    """
    pk에 해당하는 Video 인스턴스를 리턴
    템플릿은 video/bookmark_detail.html사용
    extra
        get_object_or_404를 써봅니다
    """
    video = Video.objects.get(pk=pk)
    context = {
        'video': video
    }
    return render(request, 'video/bookmark_detail.html', context)

@login_required
def bookmark_delete(request, pk):
    video = Video.objects.get(pk=pk)
    video.delete()

    return redirect('video:bookmark_list')
