from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CodePost

# Create your views here.

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username alreddy exits')
        else:
            User.objects.create_user(username=username, password=password)
            messages.success(request, 'User register successfully')
            return redirect('login')
    return render(request, 'data/register.html')

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid cerdentials')
    return render(request, 'data/login.html')

@login_required(login_url='login')
def home(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        if code:
            CodePost.objects.create(user=request.user, code=code)

    posts = CodePost.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'data/home.html', {
        'posts': posts
    })

def user_logout(request):
    logout(request)
    return redirect('login')

'''
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CodePost

@login_required(login_url='login')
def home(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        if code:
            CodePost.objects.create(user=request.user, code=code)

    posts = CodePost.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'data/home.html', {
        'posts': posts
    })
'''