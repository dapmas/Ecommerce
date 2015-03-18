from django.conf.urls import patterns,url
from website import views


urlpatterns = patterns('',url(r'^index/$', views.index, name='index'))


