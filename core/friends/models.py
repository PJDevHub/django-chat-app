from django.db import models
from django.conf import settings


# Create your models here.


User = settings.AUTH_USER_MODEL


class FriendRequest(models.Model):

    sender = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)

    receiver = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)

    status = models.CharField(max_length=10, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    ], default='pending')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} → {self.receiver}"