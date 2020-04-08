from django.conf.urls import url

from shop import views

urlpatterns = [
    url(r'^add/$', views.add, name='add_shop'),
    url(r'^list/$', views.list, name='list_shop'),
    url(r'^show/(?P<id>[0-9A-Za-z_\-]+)/$', views.show, name='show_shop'),
    url(r'^modify/(?P<id>[0-9A-Za-z_\-]+)/$', views.modify, name='modify_shop'),
    url(r'^delete/(?P<id>[0-9A-Za-z_\-]+)/$', views.delete, name='del_shop'),

]
