"""hackovid URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from shop import views

urlpatterns = [
    url(r'^add/$', views.add, name='add_shop'),
    url(r'^list/$', views.list, name='list_shop'),
    url(r'^show/(?P<id>[0-9A-Za-z_\-]+)/$', views.show, name='show_shop'),
    url(r'^modify/(?P<id>[0-9A-Za-z_\-]+)/$', views.modify, name='modify_shop'),
    url(r'^shop_admins/(?P<id>[0-9A-Za-z_\-]+)/list$', views.list_admins, name='list_shop_admins'),
    url(r'^shop_admins/(?P<id>[0-9A-Za-z_\-]+)/delete/(?P<idA>[0-9A-Za-z_\-]+)$', views.delete_admin, name='delete_shop_admins'),

    url(r'^delete/(?P<id>[0-9A-Za-z_\-]+)/$', views.delete, name='del_shop'),
    url(r'^schedules/(?P<id>[0-9A-Za-z_\-]+)/list/$', views.list_schedule, name='list_schedule'),
    url(r'^schedules/(?P<id>[0-9A-Za-z_\-]+)/add/$', views.add_schedule, name='add_schedule'),
    url(r'^schedules/(?P<id>[0-9A-Za-z_\-]+)/delete/(?P<idS>[0-9A-Za-z_\-]+)$', views.delete_schedule, name='del_schedule'),

]
