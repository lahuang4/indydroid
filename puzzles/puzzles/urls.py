from django.conf.urls import patterns, url

from puzzles import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^(?P<puzzle_display_id>\d+)/$', views.detail, name='detail'),
        url(r'^(?P<puzzle_display_id>\d+)/submit/$', views.submit, name='submit'),
        url(r'^login/$', views.user_login, name='login'),
        url(r'^logout/$', views.user_logout, name='logout'),
)
