from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from hackovid.utils import reverse
from shop import forms
from shop.models import Shop
from user import models


def add(request):

    # if user is already logged, no need to log in
    if not request.user.is_authenticated or not request.user.is_shopAdmin:
        return HttpResponseRedirect(reverse('root'))

    # if this is a POST request we need to process the form data
    if request.method == 'POST':

        # create a form instance and populate it with data from the request:
        form = forms.ShopForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            shop = form.save(commit=False)
            shop.save()
            shop.admins.add(request.user)
            return HttpResponseRedirect(reverse('root'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = forms.ShopForm()
    return render(request, 'shopform.html', {'form': form})


def list(request):

    # if user is already logged, no need to log in
    if not request.user.is_authenticated or not request.user.is_shopAdmin:
        return HttpResponseRedirect(reverse('root'))

    shopsList = Shop.objects.filter(admins__id__contains=request.user.id)
    return render(request, 'shoplist.html', {'shops': shopsList})


def modify(request, id):
    print(id)
    if not request.user.is_authenticated or not request.user.is_shopAdmin:
        return HttpResponseRedirect(reverse('root'))

    #shop = Shop.objects.filter(id=id)

    return render(request, 'shoplist.html', {'shops': []})