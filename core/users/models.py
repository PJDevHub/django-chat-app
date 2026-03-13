from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.



class User(AbstractUser):

    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)

    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)

    last_seen = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
    


class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    is_online = models.BooleanField(default=False)

    last_seen = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username