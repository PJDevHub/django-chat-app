from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Message
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

@login_required
def chat_history(request, user_id):

    other_user = User.objects.get(id=user_id)

    messages = Message.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    ).order_by("timestamp")

    data = []

    for msg in messages:
        data.append({
            "sender": msg.sender.username,
            "message": msg.message,
            "time": msg.timestamp.strftime("%H:%M")
        })

    return JsonResponse({"messages": data})


@login_required
def mark_seen(request, user_id):

    Message.objects.filter(
        sender_id=user_id,
        receiver=request.user,
        status="delivered"
    ).update(status="seen")

    return JsonResponse({"status": "ok"})



@login_required
def mark_seen(request, user_id):

    Message.objects.filter(
        sender_id=user_id,
        receiver=request.user,
        status="delivered"
    ).update(status="seen")

    return JsonResponse({"status": "ok"})


@csrf_exempt
def upload_file(request):

    if request.method == "POST":

        file = request.FILES["file"]

        path = default_storage.save(f"chat_files/{file.name}", file)

        return JsonResponse({
            "file_url": f"/media/{path}"
        })
        
        
def recent_chats(request):

    user = request.user

    users = User.objects.exclude(id=user.id)

    chat_list = []

    for u in users:

        last_msg = Message.objects.filter(
            Q(sender=user, receiver=u) | Q(sender=u, receiver=user)
        ).order_by("-created_at").first()

        unread = Message.objects.filter(
            sender=u,
            receiver=user,
            status="sent"
        ).count()

        if last_msg:

            chat_list.append({
                "user_id": u.id,
                "name": u.username,
                "last_message": last_msg.message,
                "time": last_msg.created_at.strftime("%H:%M"),
                "unread": unread
            })

    return JsonResponse({
        "chats": chat_list
    })