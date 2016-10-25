from django.conf.urls import url
from video import views

urlpatterns = [
    url(r'^bookmark/list/$', views.bookmark_list, name='bookmark_list'),
    url(r'^bookmark/add/$', views.bookmark_add, name='bookmark_add'),
    url(r'^bookmark/delete/(?P<pk>\d+)/$', views.bookmark_delete, name='bookmark_delete'),
    url(r'^bookmark/(?P<pk>\d+)/$', views.bookmark_detail, name='bookmark_detail'),
    url(r'^search/$', views.search, name='search'),
    url(r'^list/$', views.bookmark_list, name='list'),

]
