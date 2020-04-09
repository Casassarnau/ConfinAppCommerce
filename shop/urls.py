from django.conf.urls import url

from shop import views

urlpatterns = [
    url(r'^add/$', views.add, name='add_shop'),
    url(r'^list/$', views.list, name='list_shop'),
    url(r'^show/(?P<id>[0-9A-Za-z_\-]+)/$', views.show, name='show_shop'),
    url(r'^modify/(?P<id>[0-9A-Za-z_\-]+)/$', views.modify, name='modify_shop'),
    url(r'^delete/(?P<id>[0-9A-Za-z_\-]+)/$', views.delete, name='del_shop'),
    url(r'^schedules/(?P<id>[0-9A-Za-z_\-]+)/list/$', views.listS, name='list_schedule'),
    url(r'^schedules/(?P<id>[0-9A-Za-z_\-]+)/add/$', views.addS, name='add_schedule'),
    url(r'^schedules/(?P<id>[0-9A-Za-z_\-]+)/delete/(?P<idS>[0-9A-Za-z_\-]+)$', views.deleteS, name='del_schedule'),

]
