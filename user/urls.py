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
from django.urls import reverse_lazy
from django.views.generic import RedirectView

from user import views


urlpatterns = [
    url(r'^login/$', views.login, name='user_login'),
    url(r'^register/$', RedirectView.as_view(url=reverse_lazy('user_register_client')),
        name='user_register'),
    url(r'^register/client$', views.register_client, name='user_register_client'),
    url(r'^register/shop_admin$', views.register_shop_admin, name='user_register_shop_admin'),
    url(r'^logout/$', views.logout, name='user_logout'),
]
