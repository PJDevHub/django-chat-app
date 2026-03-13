from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

User = get_user_model()

class Message(models.Model):

    STATUS_CHOICES = [
        ("sent", "Sent"),
        ("delivered", "Delivered"),
        ("seen", "Seen"),
    ]

    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="received_messages", on_delete=models.CASCADE)

    message = models.TextField(blank=True, null=True)

    file = models.FileField(upload_to="chat_files/", blank=True, null=True)

    timestamp = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="sent")

    def __str__(self):
        return f"{self.sender} -> {self.receiver}"
    
    
    
    
class Group(models.Model):

    name = models.CharField(max_length=255)

    admin = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="admin_groups"
    )

    members = models.ManyToManyField(
        User,
        related_name="chat_groups"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class GroupMessage(models.Model):

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="messages"
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    message = models.TextField(blank=True, null=True)

    file = models.FileField(
        upload_to="group_files/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} -> {self.group}"
    