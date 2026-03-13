from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Group
from .models import GroupMessage
import json


def create_group(request):

    if request.method == "POST":

        data = json.loads(request.body)

        name = data.get("name")
        members = data.get("members", [])

        group = Group.objects.create(
            name=name,
            admin=request.user
        )

        group.members.add(request.user)

        for member_id in members:
            user = User.objects.get(id=member_id)
            group.members.add(user)

        return JsonResponse({
            "status": "success",
            "group_id": group.id,
            "group_name": group.name
        })
        
def group_history(request, group_id):

    messages = GroupMessage.objects.filter(
        group_id=group_id
    ).order_by("created_at")

    data = []

    for msg in messages:
        data.append({
            "message": msg.message,
            "sender": msg.sender.username,
            "time": msg.created_at.strftime("%H:%M")
        })

    return JsonResponse({
        "messages": data
    })
    
def user_groups(request):

    groups = request.user.group_memberships.all()

    data = []

    for g in groups:

        data.append({
            "id": g.id,
            "name": g.name
        })

    return JsonResponse({
        "groups": data
    })
    
def leave_group(request, group_id):

    group = Group.objects.get(id=group_id)

    group.members.remove(request.user)

    return JsonResponse({
        "status": "left"
    })
    