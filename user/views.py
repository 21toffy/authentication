from django.shortcuts import render, redirect
from .forms import UserCreationForm, UserProfileForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages 




def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserCreationForm(data=request.POST)
        if user_form.is_valid():
            user_form.save()
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
            return redirect(reverse('user:index'))
            messages.success(request, 'Thanks for registering {}'.format(user.username))
        else:
            # user_form = UserCreationForm(data=request.GET)
            messages.error(request, user_form.errors)

            print(user_form.errors)
    else:
        user_form = UserCreationForm()
    context={'user_form':user_form,
            'registered':registered,
            }
    return render(request,'registration.html',context)


def index(request):
    return HttpResponse("<h1>hello world</h1>")



def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('user:index'))
            else:
                return HttpResponse("Your account is inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'login.html', {})