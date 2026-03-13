from django.urls import path
from . import views

urlpatterns = [

    path("create/", views.create_group, name="create_group"),

    path("my-groups/", views.user_groups, name="user_groups"),
    
    path("history/<int:group_id>/", views.group_history, name="group_history"),
    
    path("my-groups/", views.user_groups, name="user_groups"),
    
    path("leave/<int:group_id>/", views.leave_group, name="leave_group"),

]