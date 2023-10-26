from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from base.models import Topic
from base.forms import UserForm

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
@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save(commit=False)
            user.username = user.username.lower()
            form.save()
            return redirect('user-profile', pk=user.id)
    context = {'user':user, 'form':form}
    return render(request, 'base/update_user.html', context)