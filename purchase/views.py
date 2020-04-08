from django.http import HttpResponseRedirect
from django.shortcuts import render

from hackovid.utils import reverse
from shop import models as sModels


def list(request):

    # if user is already logged, no need to log in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('root'))

    shopsList = sModels.Shop.objects.all()
    return render(request, 'purcahselist.html', {'shops': shopsList})


def info(request, id):

    # if user is already logged, no need to log in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('root'))

    shopsList = sModels.Shop.objects.all()
    return render(request, 'purcahselist.html', {'shops': shopsList})