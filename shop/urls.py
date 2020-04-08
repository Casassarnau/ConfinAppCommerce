from django.conf.urls import url

from shop import views

urlpatterns = [
    url(r'^add_shop/$', views.add_shop, name='add_shop'),
    url(r'^list_shop/$', views.list_shop, name='list_shop'),
]
