from django.contrib import messages, auth
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from hackovid.utils import reverse
from user import models
from user.forms import LoginForm, RegisterForm


def login(request):

    # if user is already logged, no need to log in
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('root'))

    # if this is a POST request we need to process the form data
    if request.method == 'POST':

        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)

        # check whether it's valid:
        if form.is_valid():

            # process the data in form.cleaned_data as required
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = auth.authenticate(email=email, password=password)
            if user and user.is_active:
                auth.login(request, user)

                # redirect to a new URL:
                return HttpResponseRedirect(reverse('root'))
            else:
                form.add_error(None, 'Incorrect username or password. Please try again.')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()
    return render(request, 'userform.html', {'form': form})


def register(request):

    # if user is already logged, no need to register
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('root'))

    # if this is a POST request we need to process the form data
    if request.method == 'POST':

        # create a form instance and populate it with data from the request:
        form = RegisterForm(request.POST)
        if form.is_valid():

            # process the data in form.cleaned_data as required
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            name = form.cleaned_data['name']

            # check if user email already exists
            if models.User.objects.filter(email=email).first() is not None:
                messages.error(request, 'An account with this email already exists')
            else:

                # create user & log in new user
                user = models.User.objects.create_user(email=email, password=password, name=name)
                user = auth.authenticate(email=email, password=password)
                auth.login(request, user)
                return HttpResponseRedirect(reverse('root'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RegisterForm()
    return render(request, 'userform.html', {'form': form})


def index(request):
    return HttpResponse("Hello, world. You're at the polls index. %s")