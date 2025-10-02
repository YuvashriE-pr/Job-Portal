# jobportal/urls.py (The Main Project URLs)

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 1. The Django Admin Site URL
    path('admin/', admin.site.urls),
    
    # 2. Include the 'jobs' App URLs at the ROOT of the site.
    # This makes your Job Listings page the homepage (http://127.0.0.1:8000/).
    path('', include('jobs.urls')),
    path('logout_user/', auth_views.LogoutView.as_view(), name='logout_user'),
]

# 3. Serving Media Files (Resumes, etc.) in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


