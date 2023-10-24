from django.shortcuts import render, redirect, HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from base.models import Room, Topic, Message
from base.forms import RoomForm


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User not found')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password are incorrect')

    context = {'page': 'login'}
    return render(request, 'base/login_register.html', context)


def registerUser(request):
    form = UserCreationForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        form = UserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(username=username)
                return HttpResponse(user.username)
            except:
                user = form.save(commit=False)
                user.username = user.username.lower()
                user.save()
                login(request, user)
                return redirect('home')
        else:
            messages.error(request, 'an error occurred during registration')
    context = {'register_form': form}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')

