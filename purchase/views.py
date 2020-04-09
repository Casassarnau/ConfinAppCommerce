from cmath import sqrt

from django.db.models import Count, F, FloatField, DecimalField, Func
from django.db.models.functions import Cast
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.utils import timezone

from hackovid.utils import reverse
from purchase import forms, models
from shop import models as sModels


def list(request):
    # if user is already logged, no need to log in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('root'))
    shopsList = []
    time = ''
    if request.method == 'POST':
        form = forms.FilterForm(request.POST)
        if form.is_valid():
            location = form.cleaned_data['location']
            (latitude, longitude) = location.split(', ')
            (latitude, longitude) = (float(latitude), float(longitude))
            category = form.cleaned_data['category']
            service = form.cleaned_data['service']
            time = form.cleaned_data['time']
            todayDay = timezone.now().weekday()
            shopsList = sModels.Schedule.objects.filter(day=todayDay,
                                                        startHour__lt=time,
                                                        endHour__gt=time)
            if service and category:
                shopsList = shopsList.filter(shop__secondaryCategories__primary__in=category,
                                             shop__services__in=service)
            elif service:
                shopsList = shopsList.filter(shop__services__in=service)
            elif category:
                shopsList = shopsList.filter(shop__secondaryCategories__primary__in=category)
            shopsList = shopsList.annotate(Cpoints=Func(Cast(Count('shop__purchase') + 1, DecimalField()) *
                                                        F('shop__latitude') + F('shop__longitude') -
                                                        Cast(latitude - longitude, DecimalField()),
                                                        function='ABS')
                                           ).order_by('Cpoints')
            time = time.strftime('%H:%M')
    else:
        form = forms.FilterForm()
    if shopsList is None:
        shopsList = []

    return render(request, 'purcahselist.html', {'shops': shopsList, 'form': form, 'time': time})


def info(request, id, time_str):
    # if user is already logged, no need to log in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('root'))
    try:
        shop = sModels.Shop.objects.filter(id=id).first()
    except:
        return HttpResponse(status=404)
    if request.method == 'POST':
        time = timezone.now()
        time.strftime(time_str)
        purchase = models.Purchase(shop=shop, user=request.user, dateTime=time)
        purchase.save()

    return render(request, 'purchasedetail.html', {'shop': shop, 'time': time_str})
