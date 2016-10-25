from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'', include('blog.urls', namespace='blog')),
    url(r'^member/', include('member.urls', namespace='member')),
    url(r'^video/', include('video.urls', namespace='video')),
    url(r'^sns/', include('sns.urls', namespace='sns')),
    #Common
    url(r'^error/$', views.error, name='error')
]
