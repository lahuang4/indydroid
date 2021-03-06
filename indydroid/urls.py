from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'indydroid.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^puzzles/', include('puzzles.urls', namespace="puzzles")),
    url(r'^polls/', include('polls.urls', namespace="polls")),
    url(r'^admin/', include(admin.site.urls)),
)
