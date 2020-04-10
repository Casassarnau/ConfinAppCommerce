from cmath import sqrt

from django.db.models import Count, F, FloatField, DecimalField, Func, Q, DateTimeField
from django.db.models.functions import Cast
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.utils import timezone

from hackovid.utils import reverse
from purchase import forms, models
from shop import models as sModels
from user import models as uModels


def list(request):
    # if user is already logged, no need to log in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('root'))
    shopsList = []
    time_str = ''
    if request.method == 'POST':
        form = forms.FilterForm(request.POST)
        if form.is_valid():
            location = form.cleaned_data['location']
            if location.find(',') != -1:
                (latitude, longitude) = location.split(', ')
            else:
                latitude = 0
                longitude = 0
            (latitude, longitude) = (float(latitude), float(longitude))
            category = form.cleaned_data['category']
            service = form.cleaned_data['service']
            time = form.cleaned_data['time']
            time_str = time.strftime('%H:%M')
            dateTime = timezone.now()
            dateTime_str = dateTime.strftime('%d-%m-%Y-')
            dateTime = dateTime.strptime(dateTime_str + time_str, '%d-%m-%Y-%H:%M')
            todayDay = timezone.now().weekday()
            shopsList = sModels.Schedule.objects.filter(day=todayDay,
                                                        startHour__lt=time,
                                                        endHour__gt=time)\
                .annotate(ocupacio=Count('shop__purchase',
                                         filter=Q(shop__purchase__dateTime__lt=dateTime,
                                                  shop__purchase__endTime__gt=dateTime)))
            if service and category:
                shopsList = shopsList.filter(shop__secondaryCategories__primary__in=category,
                                             shop__services__in=service)
            elif service:
                shopsList = shopsList.filter(shop__services__in=service)
            elif category:
                shopsList = shopsList.filter(shop__secondaryCategories__primary__in=category)
            shopsList = shopsList.annotate(Cpoints=Func(Cast(F('ocupacio') + 1, DecimalField()) *
                                                        (F('shop__latitude') + F('shop__longitude') -
                                                         Cast(latitude - longitude, DecimalField())) * 1000000,
                                                        function='ABS')
                                           ).order_by('Cpoints')

    else:
        form = forms.FilterForm()
    if shopsList is None:
        shopsList = []
    print(shopsList)
    return render(request, 'purcahselist.html', {'shops': shopsList, 'form': form, 'time': time_str})


def info(request, id, time_str):
    # if user is already logged, no need to log in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('root'))
    try:
        shop = sModels.Shop.objects.filter(id=id).first()
    except:
        return HttpResponse(status=404)
    if request.method == 'POST':
        dateTime = timezone.now()
        dateTime_str = dateTime.strftime('%d-%m-%Y-')
        dateTime = dateTime.strptime(dateTime_str + time_str, '%d-%m-%Y-%H:%M')
        dateTimeFuture = dateTime + timezone.timedelta(minutes=shop.meanTime)
        purchase = models.Purchase(shop=shop, user=request.user, dateTime=dateTime, endTime=dateTimeFuture)
        purchase.save()

    return render(request, 'purchasedetail.html', {'shop': shop, 'time': time_str})


def userList(request):
    # if user is already logged, no need to log in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('root'))

    purchaseListAll = models.Purchase.objects.all().filter(user=request.user)
    purchaseListActive = purchaseListAll.filter(dateTime__gt=timezone.now())
    viewAllText = 'Totes'
    viewActiveText = 'Actives'
    list = purchaseListActive
    text = viewAllText
    if request.method == 'POST':
        all = request.POST.get("value", "")
        if all == viewActiveText:
            list = purchaseListActive
        else:
            text = viewActiveText
            list = purchaseListAll

    return render(request, 'purchaselistuser.html', {'list': list, 'text': text})


def infoUserPurchase(request, id):
    # if user is already logged, no need to log in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('root'))
    try:
        purchase = models.Purchase.objects.filter(id=id, user=request.user).first()
    except:
        return HttpResponse(status=404)
    date = timezone.now().date()
    if purchase.is_pending() and purchase.dateTime.date() != date:
        purchase.expire()
        purchase.save()
    base_url = request.build_absolute_uri().split('purchase')[0]
    url = base_url[:-1] + reverse('qr_read', kwargs={'id': purchase.id})
    print(url)
    return render(request, 'purchasedetailhistory.html', {'purchase': purchase, 'qrurl': url})


def qrreaded(request, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('root'))
    try:
        purchase = models.Purchase.objects.filter(id=id, user=request.user).first()
    except:
        return HttpResponse(status=404)
    date = timezone.now().date()
    if purchase.is_pending() and purchase.dateTime.date() != date:
        purchase.expire()
        purchase.save()
        return HttpResponseRedirect(reverse('root'))
    purchase.accept()
    purchase.save()
    user = uModels.User.objects.filter(id=purchase.user.id).annotate(count=Count('purchase',
                                                                                 filter=Q(purchase__status='A')))
    return render(request, 'qr.html', {'purchase': purchase, 'user': user})