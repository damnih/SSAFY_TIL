from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from .models import User

# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('posts:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/signup.html', context)

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('posts:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)

def logout(request):
    auth_logout(request)
    return redirect('posts:index')

def profile(request, username):
    user = User.objects.get(username=username)
    context = {
        'user': user
    }
    return render(request, 'accounts/profile.html', context)

# 문제 5 팔로우 기능 오류 
def follow(request, user_pk):
    # user = User.objects.get(pk=user_pk)
    you = User.objects.get(pk=user_pk)
    me = request.user 
    if me.is_authenticated:
        if me != you: 
            if me in you.followers: 
                you.followers.remove(me) 
            else: 
                you.followers.add(me) 
    
    return redirect('accounts:profile', you.username) 

def following(request, user_pk):
    user = User.objects.get(pk=user_pk)
    context = {
        'user': user
    }
    return render(request, 'accounts/following.html', context)

def followers(request, user_pk):
    user = User.objects.get(pk=user_pk)
    context = {
        'user': user
    }
    return render(request, 'accounts/followers.html', context)