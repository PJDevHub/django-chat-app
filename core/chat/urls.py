from django.urls import path
from . import views

urlpatterns = [
    path("history/<int:user_id>/", views.chat_history, name="chat_history"),
    path("seen/<int:user_id>/", views.mark_seen, name="mark_seen"),
    path("seen/<int:user_id>/", views.mark_seen, name="mark_seen"),
    path("upload/", views.upload_file, name="upload_file"),
]