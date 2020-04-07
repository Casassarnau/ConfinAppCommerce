from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from hackovid.utils import reverse
from shop import forms


def add_shop(request):

    # if user is already logged, no need to log in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('root'))

    # if this is a POST request we need to process the form data
    if request.method == 'POST':

        # create a form instance and populate it with data from the request:
        form = forms.ShopForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            shop = form.save(commit=False)
            # TODO: Add the shop to the admin user.
            # request.user.shop = shop
            shop.save()
            return HttpResponseRedirect(reverse('root'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = forms.ShopForm()
    return render(request, 'shopform.html', {'form': form})
