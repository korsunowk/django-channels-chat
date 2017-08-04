from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from chat_django import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('chat.urls')),
    url('^accounts/', include('django.contrib.auth.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_URL)
