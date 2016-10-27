from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.album_list, name='album_list'),
    url(r'^(?P<album_pk>[0-9]+)/$', views.album_detail, name='album_detail'),
    url(r'^photo/like/(?P<photo_pk>[0-9]+)/$', views.photo_like, name='photo_like'),
    url(r'^photo/dislike/(?P<photo_pk>[0-9]+)/$', views.photo_dislike, name='photo_dislike'),
    url(r'^edit/(?P<album_pk>[0-9]+)/$', views.album_edit, name='album_edit'),
    url(r'^photo/delete/(?P<photo_pk>[0-9]+)/$', views.photo_delete, name='photo_delete'),
    # url(r'^comment/add/(?P<post_pk>[0-9]+)/$', views.comment_add, name='comment_add'),
]
