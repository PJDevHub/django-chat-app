from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def home(request):
    return redirect('/users/dashboard/')

urlpatterns = [
    path('', home),  # root path
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('friends/', include('friends.urls')),
]