from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "sender",
        "receiver",
        "message",
        "file",
        "status",
        "timestamp",
    )

    list_filter = (
        "status",
        "timestamp",
    )

    search_fields = (
        "sender__username",
        "receiver__username",
        "message",
    )

    ordering = ("-timestamp",)