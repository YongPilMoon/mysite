from django.conf.urls import url
from .import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^facebook/friends_ranking/$', views.update_friends_ranking, name='friends_ranking'),
    url(r'^facebook/show_friends_ranking/$', views.show_friends_ranking, name='show_friends_ranking'),
    url(r'^facebook/show_mypost/$', views.show_mypost, name='show_mypost'),
]