from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
# Create your views here.

def main(request):
    return render(request, "users/main.html")


def signup(request):
    #POST method로 signup
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth.login (request, user)
            return redirect ('users:main')
        else:
            return redirect ('users:signup')   
   
    #GET method로 signup
    else:
        form = SignupForm()
        ctx = {
            'form': form,
        }
        return render(request, 'users/signup.html', ctx)
        

def login(request):
    if request.method == "POST":
        form = AuthenticationForm (request, request.POST)
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            return redirect('users:main')
        else:
            ctx = {
                'form': form,
            }
            return render (request, 'users/login.html', ctx)
    else:
        form = AuthenticationForm()
        ctx = {
            'form': form,
        }
        return render (request, 'users/login.html', ctx)



def logout(request):
    auth.logout(request)
    return redirect ('users:main')