from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

from .models import User, Topic, Room, Message
from .forms import UserForm, UserCreationForm, RoomForm, MessageForm
from .utils import create_user_and_send_verification_email, activate_user


def login_page(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password does not exist')

    context = {
        'page': page,
    }
    return render(request, 'base/login_registration.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')


def register_user(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already authenticated!')
        return redirect('user_profile', pk=request.user.id)

    elif request.method == 'POST':
        form = UserCreationForm(request.POST)
        email = request.POST.get('email')
        user = User.objects.filter(email=email, is_active=False).first()
        if user is not None:
            time_difference = timezone.now() - user.activation_sent_at
            remaining_time = 5 - int(time_difference.total_seconds() / 60)
            if time_difference < timedelta(minutes=5):
                messages.error(
                    request, f"Please wait {remaining_time} minutes before requesting another activation link.")
            else:
                user.delete()
                if form.is_valid():
                    create_user_and_send_verification_email(
                        request, form, 'emails/account_verification_email.html'
                    )
                    messages.success(
                        request, f"A new verification link has been sent to your email.<br>Please check your inbox or spam folder."
                    )
        else:
            if form.is_valid():
                create_user_and_send_verification_email(
                    request, form, 'emails/account_verification_email.html')
                messages.success(
                    request, f"Your Email verification link has been successfully sent.<br>Please click it to complete the verification process.")
                return redirect('login')
            else:
                messages.error(request, 'An error occured during registration')
    else:
        form = UserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'base/login_registration.html', context)


def activate(request, uidb64, token):
    # Activate the user by setting the is_active status to True
    user = activate_user(uidb64, token)

    if user is not None and timezone.now() - user.activation_sent_at < timedelta(minutes=5):
        messages.success(
            request, 'Congratulations! Your account is activated.')
    else:
        messages.error(request, 'Activation link is invalid or has expired.')
        return redirect('home')
    return redirect('user_profile', pk=user.id)


@login_required(login_url='login')
def edit_user(request):
    user = request.user
    form = UserForm(instance=request.user)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile is updated.')
            return redirect('user_profile', pk=user.id)
        else:
            messages.error(request, 'Something went wrong during the update.')
    context = {
        'form': form
    }
    return render(request, 'base/edit_user.html', context)


@login_required(login_url='login')
def user_profile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {
        'user': user,
        'rooms': rooms,
        'room_messages': room_messages,
        'topics': topics,
    }
    return render(request, 'base/profile.html', context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q),
    )

    context = {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count,
        'room_messages': room_messages,
    }
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == 'POST':
        Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body'),
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    context = {
        'room': room,
        'room_messages': room_messages,
        'participants': participants,
    }
    return render(request, 'base/room.html', context)

# Room CRUD


@login_required(login_url='login')
def create_room(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic').capitalize()
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.save()
        return redirect('home')
    context = {
        'form': form,
        'topics': topics,
    }
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic').capitalize()
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.topic = topic
        room.name = request.POST.get('name')
        room.description = request.POST.get('description')
        room.save()
        return redirect('room', pk=room.id)
    context = {
        'form': form,
        'topics': topics,
        'room': room,
    }
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def delete_room(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})

# Message CRUD


@login_required(login_url='login')
def edit_message(request, pk):
    message = Message.objects.get(id=pk)
    form = MessageForm(instance=message)

    if request.user != message.user:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            message.is_edited = True
            message.save()
            form.save()
            return redirect('room', pk=message.room.id)
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def delete_message(request, pk):
    message = Message.objects.get(id=pk)
    room_id = message.room.id
    if request.user != message.user:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        message.delete()
        return redirect('room', pk=room_id)
    return render(request, 'base/delete.html', {'obj': message})


def topics_page(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)

    return render(request, 'base/topics.html', {'topics': topics})


def activity_page(request):
    room_messages = Message.objects.all()

    return render(request, 'base/activity.html', {'room_messages': room_messages})
