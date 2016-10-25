import requests
import json
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse

from collections import Counter

from apis import facebook
from sns.models import FriendsRank

__all__ = [
    'update_friends_ranking',
    'show_friends_ranking',
    'show_mypost'
]


def update_friends_ranking(request):
    if request.method == 'GET':
        if request.GET.get('error'):
            return HttpResponse('사용자 로그인 거부')
        if request.GET.get('code'):
            redirect_uri = 'http://{host}{url}'.format(
                host=request.META['HTTP_HOST'],
                url=reverse('sns:friends_ranking')
            )
            code = request.GET.get('code')
            access_token = facebook.get_access_token(code, redirect_uri)
            user_id = facebook.get_user_id_from_token(access_token)
            url_request_feed = 'https://graph.facebook.com/v2.8/{user_id}/feed?fields=' \
                               'comments{{from,comments}}&' \
                               'access_token={access_token}'.format(
                                user_id=user_id,
                                access_token=access_token,
                                )

            r = requests.get(url_request_feed)
            dict_feed_info = r.json()
            json_data = json.dumps(dict_feed_info, indent=2)

            comment_list = []
            for feed in dict_feed_info.get('data'):
                if feed.get('comments'):
                    for comment in feed.get('comments').get('data'):
                        comment_list.append(comment)

            # print(comment_list)
            counter = Counter()
            id_list = [comment.get('from', {}).get('id') for comment in comment_list]
            for id in id_list:
                counter[id] += 1

            most_list = counter.most_common()
            req_id_list = list(set(id_list))
            str_req_id_list = ','.join(req_id_list)

            uri_request_user_info_list = 'https://graph.facebook.com/v2.8/?ids={ids}&' \
                                         'fields=cover,email,picture.width(150).height(150),name&' \
                                         'access_token={access_token}'.format(
                                            ids=str_req_id_list,
                                            access_token=access_token,
                                         )
            r = requests.get(uri_request_user_info_list)
            dict_friends_info = r.json()
            json_friends_info = json.dumps(dict_friends_info, indent=2)

            most_dict_list = []
            for item in most_list:
                id = item[0]
                for k in dict_friends_info:
                    if k == id and k != user_id:
                        most_dict_list.append({
                            'info': dict_friends_info[k],
                            'number': item[1]
                        })

            context = {
                'most_dict_list': most_dict_list
            }
            return render(request, 'sns/facebook/friends_ranking.html', context)
        elif request.method == 'POST':
            import ast
            str_item_list = request.POST.getlist('item')

            for str_item in str_item_list:
                item = ast.listeral_eval(str_item)
            print("string item: ", item)

def show_friends_ranking(request):
    friends = FriendsRank.objects.all().order_by('-comment_count')
    context = {
        'friends': friends
    }

    return render(request, 'sns/show_friends_ranking.html', context)


def show_mypost(request):
    if request.GET.get('error'):
        return HttpResponse('사용자 거부')
    if request.GET.get('code'):
        redirect_uri = 'http://{host}{url}'.format(
            host=request.META['HTTP_HOST'],
            url=reverse('sns:show_mypost')
        )
        code = request.GET.get('code')
        access_token = facebook.get_access_token(code, redirect_uri)
        user_id = facebook.get_user_id_from_token(access_token)
        url_request_post = 'https://graph.facebook.com/v2.8/{user_id}/posts?' \
                           'access_token={access_token}'.format(
                            user_id=user_id,
                            access_token=access_token,
                            )
        r = requests.get(url_request_post)
        dict_post_info = r.json()
        print(dict_post_info)

        post_data_list = []
        for post in dict_post_info['data']:
            if post.get('message'):
                post_data_list.append({
                     'message':post['message'],
                     'created_time':post['created_time'],
                    })

        context ={
            'posts': post_data_list,
        }
        return render(request, 'sns/show_my_posts.html', context)
