from django.http import HttpResponseRedirect
from django.urls import reverse


def root_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user_login'))
    elif request.user.is_shopAdmin:
        return HttpResponseRedirect(reverse('list_shop'))
    else:
        return HttpResponseRedirect(reverse('purchase_list'))
