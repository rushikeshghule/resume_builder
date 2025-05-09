"""
URL configuration for resumecraft project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponse

def login_redirect(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return redirect('home')
        
def health_check(request):
    """Simple health check endpoint for Railway deployment"""
    return HttpResponse("OK", status=200)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_redirect, name='root_redirect'),
    path('resume/', include('resume.urls')),
    path('accounts/', include('accounts.urls')),
    path('health/', health_check, name='health_check'),
]

# Add URL patterns for serving static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
