from django.conf.urls import url

from purchase import views

urlpatterns = [
    url(r'^list/$', views.list, name='purchase_list'),
    url(r'^shop/(?P<id>[0-9A-Za-z_\-]+)$', views.info, name='go_shop'),
]
