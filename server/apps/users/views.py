from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
#예진추가뷰
def mypage_myfunding(request):
    return render(request,'users/mypage_myfunding.html')
def mypage_participated(request):
    return render(request,'users/mypage_participated.html')

#채연추가뷰
def birth_input(request):
    return render(request,'users/birth_input.html')
def signup(request):
    #POST method로 signup
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth.login (request, user)
            return redirect ('fundings:main')
        else:
            return redirect ('users:signup')   
   
    #GET method로 signup
    else:
        form = SignupForm()
        ctx = {
            'form': form,
        }
        return render(request, 'users/users_signup.html', ctx)
        

def login(request):
    if request.method == "POST":
        form = AuthenticationForm (request, request.POST)
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            return redirect('fundings:main')
        else:
            ctx = {
                'form': form,
            }
            return render (request, 'users/users_login.html', ctx)
    else:
        form = AuthenticationForm()
        ctx = {
            'form': form,
        }
        return render (request, 'users/users_login.html', ctx)



def logout(request):
    auth.logout(request)
    return redirect ('fundings:main')
