from django.urls import path
from .views import *

app_name = 'posts'

urlpatterns = [
    path('', post_list_view, name='post-list'),
    path('create', post_create_view, name='post-create'),
    path('action/', post_action_view),

    path('<int:post_id>/', post_detail_view, name='post-details'),
    path('<int:post_id>/delete', post_delete_view, name='post-delete'),
]

