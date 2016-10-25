from django.db.models import Q
from django.shortcuts import render, HttpResponse, redirect
from video.apis.youtube import youtube_search, youtube_video
from video.models import Video

__all__ = ['search']

def search(request):
    context = {}
    keyword = request.GET.get('keyword')
    page_token = request.GET.get('page_token')

    if keyword:
        search_response = youtube_search(keyword, page_token)

        video_id_list = []
        for item in search_response['items']:
            if item['id'].get('videoId'):
                video_id_list.append(item['id']['videoId'])

        video_response = youtube_video(video_id_list, search_response)

        video_id_list = [item['id'] for item in video_response['items']]
        exist_list = Video.objects.filter(
            Q(youtube_id__in=video_id_list) &
            Q(users__pk=request.user.pk)
        )
        exist_id_list = [video.youtube_id for video in exist_list]
        for item in video_response['items']:
            cur_video_id = item['id']
            if cur_video_id in exist_id_list:
                item['is_exist'] = True

        response = video_response
        context['keyword'] = keyword
        context['response'] = response
    return render(request, 'video/search.html', context)