from django.db import IntegrityError
from django.db.models import Count, F, DecimalField, Func, Q
from django.db.models.functions import Cast
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.utils import timezone

from hackovid import settings
from hackovid.utils import reverse
from purchase import forms, models
from shop import models as sModels
from user import models as uModels


def list(request):
    # if user is not logged in redirect him
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('root'))
    shopsList = []
    time_str = ''
    llista = False
    if request.method == 'POST':

        form = forms.FilterForm(request.POST)

        if form.is_valid():
            location = form.cleaned_data['location']

            # checks if the location data is in correct format and gets the latitude and longitude
            if location.find(',') != -1:
                (latitude, longitude) = location.split(', ')
            else:
                latitude = 0
                longitude = 0
            (latitude, longitude) = (float(latitude), float(longitude))
            category = form.cleaned_data['category']
            service = form.cleaned_data['service']

            # gets the hour from form and adds the current day
            time = form.cleaned_data['time']
            time_str = time.strftime('%H:%M')
            dateTime = timezone.now()
            dateTime_str = dateTime.strftime('%d-%m-%Y-')
            dateTime = dateTime.strptime(dateTime_str + time_str, '%d-%m-%Y-%H:%M')
            todayDay = timezone.now().weekday()

            # filters if there's a shop open in this hour
            shopsList = sModels.Schedule.objects.filter(day=todayDay,
                                                        startHour__lte=time,
                                                        endHour__gt=time)

            # filters by search by category and services
            if service and category:
                shopsList = shopsList.filter(shop__secondaryCategories__primary__in=category,
                                             shop__services__in=service)
            elif service:
                shopsList = shopsList.filter(shop__services__in=service)
            elif category:
                shopsList = shopsList.filter(shop__secondaryCategories__primary__in=category)

            # orders by the nearest-lessOccupied shops and filters by nearest ones, gets 20 of them in order for the
            # user to have a good experience
            shopsList = shopsList.annotate(distance=(Func((F('shop__latitude') -
                                                           Cast(latitude, DecimalField())) * 111000,
                                                          function='ABS') +
                                                     Func((F('shop__longitude') -
                                                           Cast(longitude, DecimalField())) * 111000,
                                                          function='ABS')) / 70).filter(distance__lt=60) \
                                 .annotate(ocupacio=Count('shop__purchase',
                                                          filter=Q(shop__purchase__dateTime__lte=dateTime,
                                                                   shop__purchase__endTime__gt=dateTime)),
                                           Cpoints=Cast(F('ocupacio') + 1, DecimalField()) * F('distance')) \
                                 .order_by('Cpoints')[:20]
            llista = True
    else:
        form = forms.FilterForm()
    if shopsList is None:
        shopsList = []
    return render(request, 'purcahselist.html', {'shops': shopsList, 'form': form, 'time': time_str, 'llista': llista})


def info(request, id, time_str):
    # if user is not logged in redirect him
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('root'))

    # gets the shop
    try:
        shop = sModels.Shop.objects.filter(id=id).first()
    except:
        return HttpResponse(status=404)
    if request.method == 'POST':
        # gets the time by the url
        dateTime = timezone.now()
        dateTime_str = dateTime.strftime('%d-%m-%Y-')
        dateTime = dateTime.strptime(dateTime_str + time_str, '%d-%m-%Y-%H:%M')
        dateTimeFuture = dateTime + timezone.timedelta(minutes=shop.meanTime)

        # tries to save the purchase, in case of unique violation redirect to user_list
        try:
            purchase = models.Purchase(shop=shop, user=request.user, dateTime=dateTime, endTime=dateTimeFuture,
                                       status=models.PCH_PENDING)
            purchase.save()
            return HttpResponseRedirect(reverse('purchase', kwargs={'id': purchase.id}))
        except IntegrityError:
            pass

    # order schedules of the shop by day and startHour
    schedule = shop.schedule.all().order_by('day', 'startHour')
    return render(request, 'purchasedetail.html', {'shop': shop, 'time': time_str, 'schedule': schedule})


def userList(request):
    # if user is not logged in redirect him
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('root'))

    # gets the purchase list
    purchaseListAll = models.Purchase.objects.filter(user=request.user).order_by('-dateTime')
    purchaseListActive = purchaseListAll.filter(status=models.PCH_PENDING)
    viewAllText = 'Totes'
    viewActiveText = 'Pendents'

    # change the list viewed by pending or all and the button text as well
    list = purchaseListActive
    text = viewAllText
    if request.method == 'POST':
        all = request.POST.get("value", "")
        if all == viewActiveText:
            list = purchaseListActive[:20]
        else:
            text = viewActiveText
            list = purchaseListAll[:20]

    return render(request, 'purchaselistuser.html', {'list': list, 'text': text})


def infoUserPurchase(request, id):
    # if user is not logged in redirect him
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('root'))

    # gets the purchase
    try:
        purchase = models.Purchase.objects.filter(id=id, user=request.user).first()
    except:
        return HttpResponse(status=404)

    # checks if the purchase pending is on day, else put it on expired
    date = timezone.now().date()
    if purchase.is_pending() and purchase.dateTime.date() != date:
        purchase.expire()
        purchase.save()

    # makes url for the qr code
    base_url = getattr(settings, 'APP_DOMAIN', 'localhost:8000')
    url = base_url + reverse('qr_read', kwargs={'id': purchase.id})
    return render(request, 'purchasedetailhistory.html', {'purchase': purchase, 'qrurl': url})


def qrreaded(request, id):
    # if user is not logged in redirect him
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('root'))

    # gets purchase
    try:
        purchase = models.Purchase.objects.filter(id=id).first()
    except:
        return HttpResponse(status=404)

    # if user has no permissions to accept the purchase, gets not found
    if not purchase.is_pending() or request.user not in purchase.shop.admins.all() and \
            request.user.id != purchase.shop.owner.id:
        return HttpResponse(status=404)

    # checks again if the purchase is on day, just in case
    date = timezone.now().date()
    if purchase.is_pending() and purchase.dateTime.date() != date:
        purchase.expire()
        purchase.save()
        return HttpResponseRedirect(reverse('root'))

    # accept the purchase
    purchase.accept()
    purchase.save()

    # count number of purchases accepted from the user
    user = uModels.User.objects.filter(id=purchase.user.id).annotate(count=Count('purchase',
                                                                                 filter=Q(purchase__status='A',
                                                                                          purchase__shop=purchase.shop
                                                                                          )))
    return render(request, 'qr.html', {'purchase': purchase, 'user': user})
