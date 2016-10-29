from django.conf.urls import url
from . import views
from . import ajax
urlpatterns = [
    url(r'^$', views.album_list, name='album_list'),
    url(r'^(?P<album_pk>[0-9]+)/$', views.album_detail, name='album_detail'),
    url(r'^photo/like/(?P<photo_pk>[0-9]+)/(?P<like_type>\w+)/$', views.photo_like, name='photo_like'),
    url(r'^edit/(?P<album_pk>[0-9]+)/$', views.album_edit, name='album_edit'),
    url(r'^photo/delete/(?P<photo_pk>[0-9]+)/$', views.photo_delete, name='photo_delete'),
    url(r'^add/$', views.album_add, name='album_add'),
    url(r'^photo/multi/add/(?P<album_pk>[0-9]+)$', views.photo_multi_add, name='photo_multi_add'),
    url(r'^ajax/like/(?P<photo_pk>[0-9]+)/(?P<like_type>\w+)/$', ajax.ajax_photo_like, name='ajax_photo_like'),
]
