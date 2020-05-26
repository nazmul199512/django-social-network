from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from posts.views import *
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('react/', TemplateView.as_view(template_name='react/react_via_django.html')),

    path('posts', post_list_view),
    path('posts/create', post_create_view),
    path('posts/<int:post_id>', post_detail_view),
    path('api/posts/', include('posts.urls', namespace='posts')),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


