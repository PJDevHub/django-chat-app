from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import FriendRequest

User = get_user_model()


@login_required
def send_request(request, user_id):

    receiver = get_object_or_404(User, id=user_id)

    FriendRequest.objects.get_or_create(
        sender=request.user,
        receiver=receiver
    )

    return redirect("dashboard")


@login_required
def accept_request(request, request_id):

    friend_request = get_object_or_404(FriendRequest, id=request_id)

    friend_request.status = "accepted"
    friend_request.save()

    return redirect("dashboard")


@login_required
def reject_request(request, request_id):

    friend_request = get_object_or_404(FriendRequest, id=request_id)

    friend_request.status = "rejected"
    friend_request.save()

    return redirect("dashboard")