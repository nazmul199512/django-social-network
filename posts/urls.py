from django.urls import path
from .views import *

app_name = 'posts'

urlpatterns = [

    path('', home, name='home'),
    path('post-create/', post_create_view, name='post-create'),
    path('post-list/', post_list_view, name='post-list'),
    path('post-details/<int:post_id>', post_detail_view, name='post-details'),
    path('api/post-details/action', post_action_view),
    path('api/post-details/<int:post_id>/delete', post_delete_view, name='post-delete'),
]
