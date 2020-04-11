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

from purchase import views

urlpatterns = [
    url(r'^list/$', views.list, name='purchase_list'),
    url(r'^shop/(?P<id>[0-9A-Za-z_\-]+)/(?P<time_str>[0-:_\-]+)/$', views.info, name='go_shop'),
    url(r'^user_list/$', views.userList, name='user_list'),
    url(r'^info/(?P<id>[0-9A-Za-z_\-]+)/$', views.infoUserPurchase, name='purchase'),
    url(r'^qr_accept_purchase/(?P<id>[0-9A-Za-z_\-]+)/$', views.qrreaded, name='qr_read'),
]
