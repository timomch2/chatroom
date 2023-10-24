from django.shortcuts import render, redirect, HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from base.models import Room, Topic, Message
from base.forms import RoomForm

def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room  = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def room(request, id):
    room = Room.objects.get(id=id)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', id=room.id)
    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'base/room.html', context)

@login_required(login_url='/login')
def updateRoom(request, id):
    room = Room.objects.get(id=id)
    if request.user != room.host:
        return HttpResponse('You are not allowed to edit this room')
    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RoomForm(instance=room)
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='/login')
def deleteRoom(request, id):
    room = Room.objects.get(id=id)
    if request.user != room.host:
        return HttpResponse('You are not allowed to delete this room')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})

@login_required(login_url='/login')
def deleteMessage(request, id):
    message = Message.objects.get(id=id)
    if request.user != message.user:
        return HttpResponse('You are not allowed to delete this message')
    if request.method == 'POST':
        message.delete()
        return redirect('room', id = message.room_id)
    return render(request, 'base/delete.html', {'obj': message})
