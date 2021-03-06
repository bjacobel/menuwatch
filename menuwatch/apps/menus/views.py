from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.shortcuts import render, render_to_response
from apps.menus import forms
from apps.menus import models as menumods
from random import randint
from hashlib import md5
from urllib import urlencode
import stripe
import uuid
import re


##################
## SIMPLE VIEWS ##
##################

def ExcludeView(request):
    return render(request, 'menus/exclude.html')


def AboutView(request):
    return render(request, 'menus/about.html')


def BlockView(request):
    return render(request, 'menus/block.html')

def GetReadyView(request):
    return render(request, 'menus/getready.html')


################
## MAIN VIEWS ##
################

def IndexView(request):
    photo_num = randint(0,4)
    photo = str(photo_num)+".jpg"
    
    # YEAHHH I know, I'm storing data in a view. Sue me.
    # Also this is a fairly strange way to work around python's lack of switch statements
    # All in all, not one of the best code blocks I've ever written

    credits = {
        0: ("flic.kr/pinksherbet", "http://www.flickr.com/photos/pinksherbet/2316123291/"),
        1: ("flic.kr/ginnerobot", "http://www.flickr.com/photos/ginnerobot/2523448766/"),
        2: ("flic.kr/nomadic_lass", "http://www.flickr.com/photos/nomadic_lass/5846658416/"),
        3: ("flic.kr/giovannijl-s_photohut", "http://www.flickr.com/photos/giovannijl-s_photohut/459381964/"),
        4: ("flic.kr/clarity", "http://www.flickr.com/photos/clairity/1328402515/"),
    }

    name, link = credits.get(photo_num, (None,  None))
    
    return render(request, 'menus/index.html', {
        "photo": photo,
        "name": name,
        "link": link,
        "signedin": request.user.is_authenticated(),
    })


def BrowseView(request):
    if request.user.is_authenticated():
        profile = menumods.Profile.objects.get(user__exact=int(request.user.pk))
        if profile.onboarded:
            if 'sort' in request.GET and request.GET['sort'] == 'popular':
                context = {
                    "tab": "popular",
                    "foodlist": sorted(menumods.Food.objects.all(), key=lambda x: x.num_watches(), reverse=True)[:40]
                }
            elif 'sort' in request.GET and request.GET['sort'] == 'recent':
                context = {
                    "tab": "recent",
                    "foodlist": sorted(menumods.Food.objects.exclude(last_date=None), key=lambda x: x.last_date.date, reverse=True)[:40]
                }
            elif 'sort' in request.GET and request.GET['sort'] == 'search' and 'query' in request.GET:
                foods = sorted(menumods.Food.objects.exclude(next_dates=None).filter(name__icontains=request.GET['query']), key=lambda x: x.peek_next_date())
                if len(foods) == 0:
                    foods = None
                context = {
                    "tab": "searchresults",
                    "searchstr": request.GET['query'],
                    "foodlist": foods
                } 
            elif 'sort' in request.GET and request.GET['sort'] == 'search':
                context = {
                    "tab": "search",
                    "foodlist": None
                }
            else:
                context = {
                    "tab": "upcoming",
                    "foodlist": sorted(menumods.Food.objects.exclude(next_dates=None), key=lambda x: x.peek_next_date())[:40]
                }
            return render(request, 'menus/browse.html', context)
        else:
            profile.onboarded = True
            profile.save()
            context = {
                # get five foods coming up in the next two weeks
                "popular": sorted(menumods.Food.objects.exclude(next_dates=None), key=lambda x: x.num_watches(), reverse=True)[:5]
            }
            return render(request, 'menus/onboard.html', context)

    else:
        return HttpResponseRedirect('/login?next=browse')



##########################
## AUTHENTICATION VIEWS ##
##########################

def LoginView(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/browse')
    else:
        if request.method == 'POST':
            try:
                redirect = re.search('(?:next=)(.+)', request.META.get('HTTP_REFERER')).group(1)
            except:
                redirect = "browse"
            
            form = forms.LoginForm(request.POST)

            if form.is_valid():  # All validation rules pass
                email = form.cleaned_data['email']
                pword = form.cleaned_data['pword']
                user = authenticate(username=email, password=pword)
                if user is not None and user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/'+redirect)
                else:
                    return HttpResponseRedirect('/login?next='+redirect)

            email = None  # don't try to auto-fill if the form was invalid

        else:
            form = forms.LoginForm()  # An unbound form

            if request.GET.get('e') is not None:
                email = request.GET.get('e')
            else:
                email = None

        context = {
            'form': form,
            'action': 'login',
            'email': email,
        }

        if 'HTTP_HOST' in request.META and re.search('herokuapp', request.META['HTTP_HOST']):
            context['reverify'] = True

        return render(request, 'menus/auth.html', context)


def LogoutView(request):
    if request.user.is_authenticated():
        logout(request)
    return HttpResponseRedirect('/')


def SignupView(request):
    def send_verify_mail(request, new_user):
        context = {
            'first_name': new_user.first_name,
            'verify_link': "http://menuwatch.bjacobel.com/verify?" + urlencode({'e':new_user.email, 'v':md5(new_user.email).hexdigest()}),
            'unsubscribe_link': urlencode({'u':new_user.email, 't':md5(new_user.date_joined.isoformat()).hexdigest()}),
            'email_type': 'verify',
        }
        msg = EmailMultiAlternatives(
            "Menuwatch Signup Confirmation",
            "Hi, {}! Please visit this URL to finish setting up your account. {}".format(context['first_name'], context['verify_link']),
            "Menuwatch <mail@menuwatch.bjacobel.com>",
            ["{} {} <{}>".format(new_user.first_name, new_user.last_name, new_user.email),],
        )
        msg.attach_alternative(render_to_response('menus/email.html', context).content, "text/html")
        msg.send()

    if request.user.is_authenticated():
        return HttpResponseRedirect('/browse')
    else:
        if request.method == 'POST':  # If the form has been submitted...
            form = forms.SignupForm(request.POST)  # A form bound to the POST data
            if form.is_valid():  # All validation rules pass
                email = form.cleaned_data['email']
                fname = form.cleaned_data['fname'].capitalize()
                lname = form.cleaned_data['lname'].capitalize()
                pword = form.cleaned_data['pword1']
                new_user = User.objects.create_user(email, email, pword)
                new_user.first_name = fname
                new_user.last_name = lname
                new_user.is_active = False
                new_user.save()
                profile = menumods.Profile.objects.create(user_id=new_user.pk)
                profile.save()
                send_verify_mail(request, new_user)
                return HttpResponseRedirect('/getready')  # Redirect after POST
        else:
            form = forms.SignupForm()  # An unbound form

        return render(request, 'menus/auth.html', {
            'form': form,
            'action': 'signup',
        })


def VerifyView(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/browse')
    elif request.GET and 'e' in request.GET and 'v' in request.GET:
        email = request.GET['e']
        emailhash = request.GET['v']
        if md5(email).hexdigest() == emailhash:
            to_verify = User.objects.get(username__exact=email)
            to_verify.is_active=True
            to_verify.save()
            return HttpResponseRedirect('/login?{}'.format(urlencode({'e':email})))
    else:
        return render(request, '500.html')


def RequestResetView(request):
    def send_reset_mail(request, dumb_user, newpass):
        context = {
            'first_name': dumb_user.first_name,
            'reset_link': "http://menuwatch.bjacobel.com/account/password/reset?" + urlencode({'e':dumb_user.email, 'p':newpass}),
            'unsubscribe_link': urlencode({'u':dumb_user.email, 't':md5(dumb_user.date_joined.isoformat()).hexdigest()}),
            'email_type': 'reset',
        }
        msg = EmailMultiAlternatives(
            "Menuwatch Password Reset",
            "Hi, {}! A password reset was just requested for this account.\n\nIf you didn't request a password reset, simply delete this email. If you would like to reset your password, please click below. {}".format(context['first_name'], context['reset_link']),
            "Menuwatch <mail@menuwatch.bjacobel.com>",
            ["{} {} <{}>".format(dumb_user.first_name, dumb_user.last_name, dumb_user.email),],
        )
        msg.attach_alternative(render_to_response('menus/email.html', context).content, "text/html")
        msg.send()

    if request.user.is_authenticated():
        return HttpResponseRedirect('/account/password/change')
    else:
        if request.method == 'POST':      
            form = forms.RequestResetForm(request.POST)

            if form.is_valid():  # All validation rules pass
                email = form.cleaned_data['email']
                u = User.objects.get(email__exact=email)
                if u is not None:
                    # generate a new password: a random alphanumeric string
                    newpass = uuid.uuid4().hex
                    print newpass
                    u.set_password(newpass)
                    u.save()
                    send_reset_mail(request, u, newpass)
                    return HttpResponseRedirect('/')
                else:
                    return HttpResponseRedirect('/reset')
        else:
            form = forms.RequestResetForm()  # An unbound form

        context = {
            'form': form,
            'action': 'reset',
        }

        return render(request, 'menus/auth.html', context)

###################
## ACCOUNT VIEWS ##
###################

def AccountView(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login?next=account')
    else:
        context = {
            "profile": menumods.Profile.objects.get(user__exact=int(request.user.pk)),
            'unsub_link': urlencode({'u':request.user.email, 't':md5(request.user.date_joined.isoformat()).hexdigest()}),
        }
        return render(request, 'menus/account.html', context)


def ChangePasswordView(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login?next=account')
    else:
        if request.method == 'POST':  # If the form has been submitted...
            form = forms.ChangePasswordForm(request.user, request.POST)  # A form bound to the POST data
            if form.is_valid():  # All validation rules pass
                old_pword = form.cleaned_data['pword0']
                new_pword = form.cleaned_data['pword1']
                if authenticate(username=request.user.email, password=old_pword):
                    u = User.objects.get(username__exact=request.user.email)
                    u.set_password(new_pword)
                    u.save()
                    return HttpResponseRedirect('/account')
                else:
                    return HttpResponseRedirect('/account/password')
        else:
            form = forms.ChangePasswordForm(request.user)  # An unbound form

        return render(request, 'menus/auth.html', {
            'form': form,
            'action': 'account/password/change',
        })

def ResetPasswordView(request):  # not to be confused with RequestResetView, which does what it says 
    if 'e' in request.GET and 'p' in request.GET:
        email = request.GET['e']
        old_pword = request.GET['p']

        user = authenticate(username=email, password=old_pword)
        login(request, user)

    if request.method == 'POST':  
        form = forms.ProcessResetForm(request.POST)

        if form.is_valid():  # All validation rules pass
            new_pword = form.cleaned_data['pword1']
            request.user.set_password(new_pword)
            request.user.save()
            return HttpResponseRedirect('/account')
    else:
        form = forms.ProcessResetForm()  # An unbound form

    context = {
        'form': form,
        'action': 'account/password/reset',
    }

    return render(request, 'menus/auth.html', context)

def UpgradeView(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login?next=upgrade')
    else:
        context = { "popular" : sorted(menumods.Food.objects.all(), key=lambda x: x.num_watches(), reverse=True)[:10]}
        return render(request, 'menus/upgrade.html', context)


def UnsubView(request):
    if 'u' in request.GET and 't' in request.GET:
        # need to pass a plaintext username and the MD5hashed signup date of that user
        # so you can't just randomly unsubscribe people... that would be funny
        user = request.GET['u'] 
        if md5(User.objects.get(email__exact=user).date_joined.isoformat()).hexdigest() == request.GET['t']:
            User.objects.get(email__exact=user).delete()
            return render(request, 'menus/unsubscribe.html')
        else:
            return HttpResponse("Request not authenticated", status=403)
    else:
        return HttpResponseRedirect('/')


def PaymentView(request):
    if not re.search(r'herokuapp', request.META.get('HTTP_HOST')):
        return HttpResponseRedirect("https://menuwatch.herokuapp.com/login?next=payment")

    if request.user.is_authenticated():
        if request.method == 'POST':  # If the form has been submitted...
            try:
                from settings import prod; stripe.api_key = prod.STRIPE_KEY
            except:
                from settings import dev; stripe.api_key = dev.STRIPE_KEY
            token = request.POST['stripeToken']
            try:
                charge = stripe.Charge.create(
                    amount=299, # amount in cents, again
                    currency="usd",
                    card=token,
                    description=request.user.username
                )
                proprof = menumods.Profile.objects.get(user__exact=request.user)
                proprof.pro = True
                proprof.save()
                logout(request)
                return HttpResponseRedirect("http://menuwatch.bjacobel.com/account")
            except stripe.CardError, e:
                return HttpResponse("<h1 style='text-align:center; margin-top:50px'>Your card did not validate, or was rejected. Sorry.</h1><h2><a href='http://menuwatch.bjacobel.com/account'>Back to Account ></a></h2>", status=200)
        else:
            return render(request, 'menus/payment.html')
    else:
        return HttpResponseRedirect('/login?next=payment')


###############
## API VIEWS ##
###############

@never_cache
@csrf_exempt
def AddView(request):
    if request.method == 'POST':
        if request.user is not None and request.user.is_authenticated():
            if 'food_pk' in request.POST:
                food = int(request.POST['food_pk'])
                user = int(request.user.pk)
                if menumods.Profile.objects.get(user__exact=user).can_create_new_watches():
                    try:
                        menumods.Watch.objects.create(food=menumods.Food.objects.get(pk__exact=food), owner=menumods.Profile.objects.get(user__exact=user))
                        return HttpResponse("Watch successfully created", status=201)
                    except:
                        return HttpResponse("Specified food does not exist", status=404)
                else:
                    return HttpResponse("Watch limit reached", status=431)  # 'server is unwilling to process the request' UNTIL YOU PAY ME MONIES
            else:
                return HttpResponse("No food_pk specified", status=400)
        else:
            return HttpResponse("No authenticated user present", status=403)
    else:
        return HttpResponse("I'm a teapot", status=418)


@never_cache
@csrf_exempt
def DeleteView(request):
    if request.method == 'POST':
        if request.user is not None and request.user.is_authenticated():
            if 'food_pk' in request.POST:
                food = int(request.POST['food_pk'])
                user = int(request.user.pk)
                try:
                    watch = menumods.Watch.objects.get(food__exact=food, owner__exact=menumods.Profile.objects.get(user__exact=user))
                    watch.delete()
                    return HttpResponse("Watch successfully deleted", status=200)
                except:
                    return HttpResponse("No watch mathing those parameters found", status=404)
            else:
                return HttpResponse("No food_pk specified", status=400)
        else:
            return HttpResponse("No authenticated user present", status=403)
    else:
        return HttpResponse("I'm a teapot", status=418)


@csrf_exempt
def SettingsView(request):
    if request.method == 'POST':
        if request.user is not None and request.user.is_authenticated():
            if 'setting_name' in request.POST and 'setting_value' in request.POST:
                setting_name = request.POST['setting_name']
                setting_value = request.POST['setting_value']
                user = request.user
                try:
                    user.setting_name = setting_value
                    user.save()
                    return HttpResponse("{} changed to {}".format(setting_name, setting_value), status=200)
                except:
                    return HttpResponse("Unspecified fatal API error", status=500)
            else:
                return HttpResponse("Malformed request", status=400)
        else:
            return HttpResponse("No authenticated user present", status=403)
    else:
        return HttpResponse("I'm a teapot", status=418)


#################
## DEBUG VIEWS ##
#################

def DebugEmailView(request):
    if request.user.is_staff:
        user = request.user
        context = {
            'first_name': user.first_name,
            'verify_link': "http://menuwatch.bjacobel.com/verify?" + urlencode({'e':user.email, 'v':md5(user.email).hexdigest()}),
            'unsubscribe_link': urlencode({'u':user.email, 't':md5(user.date_joined.isoformat()).hexdigest()}),
            'email_type': 'reset',
            'item_list': menumods.Food.objects.all()[:10]
        }
        return render_to_response("menus/email.html", context)

def OnboardView(request):
    if request.user.is_staff:
        context = {
            # get five foods coming up in the next two weeks
            "popular": sorted(menumods.Food.objects.exclude(next_dates=None), key=lambda x: x.num_watches(), reverse=True)[:5]
        }
        return render(request, 'menus/onboard.html', context)