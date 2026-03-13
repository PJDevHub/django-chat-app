
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


User = settings.AUTH_USER_MODEL




class Group(models.Model):

    name = models.CharField(max_length=255)

    admin = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="admin_created_groups"
    )

    members = models.ManyToManyField(
        User,
        related_name="group_memberships"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class GroupMessage(models.Model):

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="group_messages"
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="group_messages_sent"
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