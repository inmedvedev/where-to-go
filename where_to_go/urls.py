from django.contrib import admin
from django.urls import path
from .views import show_places
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', show_places)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)