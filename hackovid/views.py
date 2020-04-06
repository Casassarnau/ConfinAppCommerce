from django.http import HttpResponseRedirect
from django.urls import reverse


def root_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    return HttpResponseRedirect(reverse('index'))
