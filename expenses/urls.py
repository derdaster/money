from __future__ import unicode_literals

from django.conf.urls import patterns, url

from expenses import views



urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='home'),
#     url(r'^$', views.index, name='index'),
    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name='results'),
)