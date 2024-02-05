from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth



def logout(request):
    auth.logout(request)
    return redirect ('fundings:main')


def add_info(request):
    user = request.user
    if request.method == "POST":
        form = UserProfileUpdateForm(request.POST, request.FILES, instance = user)
        if form.is_valid():
            form.save()
            return redirect ('fundings:main')
    else:
        form = UserProfileUpdateForm(instance=user)
    ctx = {
        "form": form,
    }        
    return render (request, 'users/users_update.html', ctx)  

def redirect_view(request):
    if request.user.is_authenticated:
        # Check if it's the user's first login
        if request.user.name is None or request.user.birthday is None or request.user.nickname is None:
            return redirect('users:add_info')  # Redirect to add_info for first login
        else:
            return redirect('/')  # Redirect to home for subsequent logins
    else:
        return redirect('/')  # Redirect to home for non-authenticated users

