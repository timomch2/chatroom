from django.contrib.auth.models import User
from django.shortcuts import render
from base.models import Topic

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = { 'user': user, 'rooms':rooms, 'room_message':room_messages, 'topics':topics}
    return render(request, 'base/profile.html', context )

def myProfile(request):
    context = { 'user': request.user}
    return render(request, 'base/profile.html', context )