from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from apps.menus import forms
from random import choice
import re
import os
from settings import common


def IndexView(request):
    banner_root = common.STATIC_ROOT+"/img/banner/"
    files = filter(lambda x: x[-4:] == ".jpg", os.listdir(banner_root))
    path = choice(files)
    try:
        credits = open(banner_root+path[:-4]+".cred", 'r')
        name = credits.readline()
        link = credits.readline()
    except:
        name = None
        link = None
    path = "/static/img/banner/" + path
    return render(request, 'menus/index.html', {"path": path, "name": name, "link": link})


def BrowseView(request):
    return render(request, 'menus/browse.html')


def LoginView(request):
    return render(request, 'menus/login.html')


def LogoutView(request):
    # log 'em out
    return HttpResponseRedirect('/')


def SignupView(request):
    if request.method == 'POST':  # If the form has been submitted...
        form = forms.SignupForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            email = form.cleaned_data['email']
            fname = form.cleaned_data['fname'].capitalize()
            lname = form.cleaned_data['lname'].capitalize()
            pword = form.cleaned_data['pword1']
            uname = re.split(r'@', email)[0]
            user = User.objects.create_user(uname, email, pword)
            user.first_name = fname
            user.last_name = lname
            user.save()
            return HttpResponseRedirect('/browse/')  # Redirect after POST
    else:
        form = forms.SignupForm()  # An unbound form

    return render(request, 'menus/signup.html', {
        'form': form,
    })


def AccountView(request):
    return render(request, 'menus/account.html')


def UpgradeView(request):
    return render(request, 'menus/upgrade.html')


def ExcludeView(request):
    return render(request, 'menus/exclude.html')
