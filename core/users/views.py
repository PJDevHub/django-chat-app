from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from friends.models import FriendRequest
from .models import UserProfile



def register_view(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('login')

    else:

        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})



# login view
def login_view(request):

    if request.method == 'POST':

        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            username = user.username
        except:
            username = None

        user = authenticate(request, username=username, password=password)

        if user:

            login(request, user)

            return redirect('dashboard')

    return render(request, 'users/login.html')


# logout view

def logout_view(request):

    logout(request)

    return redirect('login')






User = get_user_model()


@login_required
def dashboard_view(request):

    users = User.objects.exclude(id=request.user.id)

    context = {
        "users": users
    }

    return render(request, "chat/dashboard.html", context)






@login_required
def dashboard_view(request):

    users = User.objects.exclude(id=request.user.id)

    received_requests = FriendRequest.objects.filter(
        receiver=request.user,
        status="pending"
    )

    sent_requests = FriendRequest.objects.filter(
        sender=request.user,
        status="pending"
    )

    context = {
        "users": users,
        "received_requests": received_requests,
        "sent_requests": sent_requests
    }

    return render(request, "chat/dashboard.html", context)

# API to Check User Status
def user_status(request, user_id):

    profile = UserProfile.objects.get(user_id=user_id)

    return JsonResponse({
        "online": profile.is_online,
        "last_seen": profile.last_seen
    })