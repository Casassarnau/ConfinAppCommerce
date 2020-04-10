from django.conf.urls import url

from purchase import views

urlpatterns = [
    url(r'^list/$', views.list, name='purchase_list'),
    url(r'^shop/(?P<id>[0-9A-Za-z_\-]+)/(?P<time_str>[0-:_\-]+)/$', views.info, name='go_shop'),
    url(r'^user_list/$', views.userList, name='user_list'),
    url(r'^info/(?P<id>[0-9A-Za-z_\-]+)/$', views.infoUserPurchase, name='purchase'),
]
