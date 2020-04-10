import os

from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.

from hackovid.utils import reverse
from shop import forms
from shop.models import Shop, Schedule
from user.models import User


def show(request, id=None):
    try:
        shop = Shop.objects.filter(id=id, owner=request.user).first()
        if shop is None:
            shop = Shop.objects.filter(id=id, admins=request.user).first()
    except:
        shop = None

    if not request.user.is_authenticated or not request.user.is_shopAdmin or shop is None:
        return HttpResponseRedirect(reverse('root'))
    schedule = shop.schedule.all().order_by('day', 'startHour')

    return render(request, 'shopview.html', {'shop': shop, 'schedule': schedule})


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


            CIF = form.cleaned_data['CIF']
            name = form.cleaned_data['name']
            s = Shop.objects.filter(CIF=CIF, name=name).first()
            if not s is None:
                form.add_error('CIF', 'Ja existeix aquesta botiga')
                return render(request, 'shopform.html', {'form': form})

            meanTime = form.cleaned_data['meanTime']
            secondaryCategories = form.cleaned_data['secondaryCategories']
            services = form.cleaned_data['services']
            photo = form.cleaned_data['photo']
            description = form.cleaned_data['description']
            map = form.cleaned_data['map']
            (lon, lat) = map.split(',')

            shop = Shop(CIF=CIF, name=name, meanTime=meanTime, latitude=lat, longitude=lon,
                       owner=request.user, photo=photo, description=description)
            shop.save()
            shop.secondaryCategories.set(secondaryCategories)
            shop.services.set(services)
            return HttpResponseRedirect(reverse('root'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = forms.ShopForm()
    return render(request, 'shopform.html', {'form': form})


def list(request):

    # if user is already logged, no need to log in
    if not request.user.is_authenticated or not request.user.is_shopAdmin:
        return HttpResponseRedirect(reverse('root'))
    shopsList = Shop.objects.filter(owner=request.user.id)
    shopsList = shopsList | Shop.objects.filter(admins__id__contains=request.user.id)
    return render(request, 'shoplist.html', {'shops': shopsList})


def modify(request, id=None):
    try:
        shop = Shop.objects.filter(id=id, owner=request.user).first()
    except:
        shop = None

    if not request.user.is_authenticated or not request.user.is_shopAdmin or shop is None:
        return HttpResponseRedirect(reverse('root'))

    if request.method == 'POST':

        # create a form instance and populate it with data from the request:
        form = forms.ShopForm(request.POST, instance=shop)

        # check whether it's valid:
        if form.is_valid():
            map = form.cleaned_data['map']
            (lon, lat) = map.split(',')
            shop = form.save()
            shop.longitude = lon
            shop.latitude = lat
            secondaryCategories = form.cleaned_data['secondaryCategories']
            services = form.cleaned_data['services']
            shop.save()
            shop.secondaryCategories.set(secondaryCategories)
            shop.services.set(services)

            return HttpResponseRedirect(reverse('root'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = forms.ShopForm(instance=shop, initial={'map': [float(shop.longitude), float(shop.latitude)]})
    return render(request, 'modifyshopform.html', {'form': form, 'id': id, 'shop': shop.photo})


def delete(request, id=None):
    try:
        shop = Shop.objects.filter(id=id, owner=request.user).first()
    except:
        shop = None

    if not request.user.is_authenticated or not request.user.is_shopAdmin or shop is None:
        return HttpResponseRedirect(reverse('root'))

    if request.method == 'POST':
        shop.delete()

    else:
        form = forms.ShopForm(instance=shop, initial={'map': [float(shop.longitude), float(shop.latitude)]})
        return render(request, 'deleteshopform.html', {'form': form, 'id': id, 'shop': shop.photo})

    return HttpResponseRedirect(reverse('root'))


def list_admins(request, id=None):
    try:
        shop = Shop.objects.filter(id=id, owner=request.user).first()
    except:
        shop = None

    if not request.user.is_authenticated or not request.user.is_shopAdmin or shop is None:
        return HttpResponseRedirect(reverse('root'))

    if request.method == 'POST':
        form = forms.AddShopAdminForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            mail = form.cleaned_data['email']
            u = User.objects.filter(email=mail).first()
            if u is None or not u.is_shopAdmin or u==request.user:
                form.add_error('email', 'No s\'ha trobat l\'usuari')
            else:
                shop.admins.add(u)
                form = forms.AddShopAdminForm()
    # if a GET (or any other method) we'll create a blank form
    else:
        form = forms.AddShopAdminForm()
    admin_list = shop.admins.all().order_by('name')
    return render(request, 'adminlist.html', {'form': form, 'admins': admin_list, 'id': id})


def delete_admin(request, id=None, idA = None):
    try:
        shop = Shop.objects.filter(id=id, owner=request.user).first()
    except:
        shop = None
    if not request.user.is_authenticated or not request.user.is_shopAdmin or shop is None:
        return HttpResponseRedirect(reverse('root'))
    shop.admins.remove(idA)
    shop.save()
    return HttpResponseRedirect(reverse('list_shop_admins', kwargs={'id': id}))



def add_schedule(request, id=None):

    try:
        shop = Shop.objects.filter(id=id, owner=request.user).first()
    except:
        shop = None
    if not request.user.is_authenticated or not request.user.is_shopAdmin or shop is None:
        return HttpResponseRedirect(reverse('root'))


    # if this is a POST request we need to process the form data
    if request.method == 'POST':

        # create a form instance and populate it with data from the request:
        form = forms.ScheduleForm(request.POST, request.FILES)

        # check whether it's valid:
        if form.is_valid():
            day = form.cleaned_data['day']

            startHour = form.cleaned_data['startHour']
            endHour = form.cleaned_data['endHour']
            list = Schedule.objects.filter(day=day,shop=shop).all()
            go = True
            for schedule in list:
                if (startHour >= schedule.startHour and startHour <= schedule.endHour) or (
                        endHour >= schedule.startHour and endHour <= schedule.endHour) or (
                        startHour >= schedule.startHour and endHour <= schedule.endHour):
                    go = False
            if not go:
                form.add_error(None,"It's overlapping with another schedue")
            else:
                sch = Schedule(shop=shop, day=day, startHour=startHour, endHour=endHour)
                sch.save()
                return HttpResponseRedirect(reverse('list_schedule', kwargs={'id':id}))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = forms.ScheduleForm()
    return render(request, 'shopform.html', {'form': form, 'id':id})

def list_schedule(request, id=None):

    # if user is already logged, no need to log in
    try:
        shop = Shop.objects.filter(id=id, owner=request.user).first()
    except:
        shop = None
    if not request.user.is_authenticated or not request.user.is_shopAdmin or shop is None:
        return HttpResponseRedirect(reverse('root'))

    scheduleList = Schedule.objects.filter(shop=shop).all()
    return render(request, 'schedulelist.html', {'schedules': scheduleList, 'id': id})




def delete_schedule(request, id=None, idS = None):
    try:
        shop = Shop.objects.filter(id=id, owner=request.user).first()
    except:
        shop = None
    if not request.user.is_authenticated or not request.user.is_shopAdmin or shop is None:
        return HttpResponseRedirect(reverse('root'))
    schedule = Schedule.objects.filter(id=idS).first()
    schedule.delete()
    return HttpResponseRedirect(reverse('list_schedule', kwargs={'id': id}))








