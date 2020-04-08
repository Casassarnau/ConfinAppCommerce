from django.http import HttpResponseRedirect
from django.shortcuts import render

from hackovid.utils import reverse
from purchase import forms
from shop import models as sModels


def list(request):

    # if user is already logged, no need to log in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('root'))
    if request.method == 'POST':
        form = forms.FilterForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data['category']
            service = form.cleaned_data['service']
            if service and category:
                shopsList = sModels.Shop.objects.filter(secondaryCategories__primary__in=category, services__in=service)
            elif service:
                shopsList = sModels.Shop.objects.filter(services__in=service)
            elif category:
                shopsList = sModels.Shop.objects.filter(secondaryCategories__primary__in=category)
            else:
                shopsList = sModels.Shop.objects.all()
        else:
            shopsList = []
    else:
        form = forms.FilterForm()
        shopsList = sModels.Shop.objects.all()
    return render(request, 'purcahselist.html', {'shops': shopsList, 'form': form})


def info(request, id):

    # if user is already logged, no need to log in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('root'))

    shopsList = sModels.Shop.objects.all()
    return render(request, 'purcahselist.html', {'shops': shopsList})