from django.shortcuts import render, redirect, HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from base.models import Room, Topic, Message
from base.forms import RoomForm


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    room_count = rooms.count()
    topics = Topic.objects.all()
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q)
    )

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'room_message':room_messages}
    return render(request, 'base/home.html', context)
