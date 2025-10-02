# jobs/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # 1. Main Job Listings (The App's Homepage)
    path('', views.job_list, name='job_list'),
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
    path('job/<int:job_id>/apply/', views.apply_job, name='apply_job'),

    # 2. Seeker Paths
    path('seeker/dashboard/', views.seeker_dashboard, name='seeker_dashboard'),
    path('register/', views.seeker_register, name='seeker_register'),
    path('applications/<int:application_id>/delete/', views.delete_application, name='delete_application'),
    path('applications/<int:application_id>/resume/', views.view_resume, name='view_resume'),

    # 3. Employer Paths
    path('employer/register/', views.employer_register, name='employer_register'),
    path('employer/dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('job/post/', views.post_job, name='post_job'),
    path('job/<int:job_id>/applications/', views.view_applications, name='view_applications'),
    path('job/edit/<int:job_id>/', views.edit_job, name='edit_job'),
    path('job/delete/<int:job_id>/', views.delete_job, name='delete_job'),

    # 4. Profile Paths
    path('profile/', views.profile_view, name='profile_view'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit_view'), # Removed duplicates

    # 5. Authentication Paths (Cleaned and consolidated)
    path('login/', auth_views.LoginView.as_view(template_name='jobs/login.html'), name='login'),
    
    # We use auth_views.LogoutView and rely on LOGOUT_REDIRECT_URL in settings.py for the redirect
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]