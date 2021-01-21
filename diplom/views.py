from django.shortcuts import render, redirect
from django.contrib import auth

def logout(request):
    auth.logout(request)
    return redirect('/')

def home(request):
    return render(request, 'index.html')
