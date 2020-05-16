from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from posts.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('api/posts/', include('posts.urls', namespace='posts')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)