from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'', include('blog.urls', namespace='blog')),
    url(r'^member/', include('member.urls', namespace='member')),
    url(r'^video/', include('video.urls', namespace='video')),
    url(r'^sns/', include('sns.urls', namespace='sns')),
    url(r'^album/', include('photo.urls', namespace='album')),

    #Common
    url(r'^error/$', views.error, name='error')
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )