import os

from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.

from hackovid.utils import reverse
from shop import forms
from shop.models import Shop


def show(request, id=None):
    try:
        shop = Shop.objects.filter(id=id, admins=request.user).first()
    except:
        shop = None

    if not request.user.is_authenticated or not request.user.is_shopAdmin or shop is None:
        return HttpResponseRedirect(reverse('root'))

    return render(request, 'shopview.html', {'shop': shop})


def add(request):

    # if user is already logged, no need to log in
    if not request.user.is_authenticated or not request.user.is_shopAdmin:
        return HttpResponseRedirect(reverse('root'))

    # if this is a POST request we need to process the form data
    if request.method == 'POST':

        # create a form instance and populate it with data from the request:
        form = forms.ShopForm(request.POST, request.FILES)

        # check whether it's valid:
        if form.is_valid():
            shop = form.save()
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


def modify(request, id=None):
    try:
        shop = Shop.objects.filter(id=id, admins=request.user).first()
    except:
        shop = None

    if not request.user.is_authenticated or not request.user.is_shopAdmin or shop is None:
        return HttpResponseRedirect(reverse('root'))

    if request.method == 'POST':

        # create a form instance and populate it with data from the request:
        form = forms.ShopForm(request.POST,instance=shop)

        # check whether it's valid:
        if form.is_valid():
            shop2 = form.save()
            shop.save()

            return HttpResponseRedirect(reverse('root'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = forms.ShopForm(instance=shop)
    return render(request, 'modifyshopform.html', {'form': form, 'id': id})


def delete(request, id=None):
    try:
        shop = Shop.objects.filter(id=id, admins=request.user).first()
    except:
        shop = None
    if not request.user.is_authenticated or not request.user.is_shopAdmin or shop is None:
        return HttpResponseRedirect(reverse('root'))
    shop.delete()
    return HttpResponseRedirect(reverse('root'))

