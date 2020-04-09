from cmath import sqrt

from django.db.models import Count, F, FloatField, DecimalField, Func
from django.db.models.functions import Cast
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone

from hackovid.utils import reverse
from purchase import forms
from shop import models as sModels


def list(request):
    # if user is already logged, no need to log in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('root'))
    shopsList = []
    if request.method == 'POST':
        form = forms.FilterForm(request.POST)
        if form.is_valid():
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
                                                        Cast(request.user.latitude - request.user.longitude,
                                                             DecimalField()),
                                                        function='ABS')
                                           ).order_by('Cpoints')
    else:
        form = forms.FilterForm()
    if shopsList is None:
        shopsList = []

    return render(request, 'purcahselist.html', {'shops': shopsList, 'form': form})


def info(request, id):
    # if user is already logged, no need to log in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('root'))

    shopsList = sModels.Shop.objects.all()
    return render(request, 'purcahselist.html', {'shops': shopsList})
