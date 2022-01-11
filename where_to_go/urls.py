from django.contrib import admin
from django.urls import path
from .views import show_main
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', show_main)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)