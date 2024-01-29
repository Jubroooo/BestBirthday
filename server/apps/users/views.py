from django.shortcuts import render, redirect

# Create your views here.

def main(request):
    return render(request, "users/main.html")