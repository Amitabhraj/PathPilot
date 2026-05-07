from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from PathPilot import views

urlpatterns = [

    path('admin/', admin.site.urls),

    path(
        'resume/',
        include('AppResume.urls')
    ),

    path(
        'user/',
        include('AppUser.urls')
    ),

    path(
        '',
        views.index,
        name='home'
    ),

] + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)