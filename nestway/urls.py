from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('favicon.ico', RedirectView.as_view(url=settings.STATIC_URL + 'images/favicon.png', permanent=True)),
]

if settings.DEBUG:
    urlpatterns += [
        path('404/', lambda request: render(request, '404.html'))
    ]

# Always serve media files via Django (WhiteNoise only handles /static/)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
