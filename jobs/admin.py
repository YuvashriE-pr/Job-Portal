# jobs/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
# We are importing UserAdmin to extend its functionality

# Import all models, including the Custom User model, from the current app's models.py
from .models import User, Job, Application, SeekerProfile, EmployerProfile 


# 1. Custom Admin for the User Model
# We customize UserAdmin to display the 'is_seeker' and 'is_employer' fields.
class CustomUserAdmin(UserAdmin):
    # This ensures is_seeker and is_employer are visible in the list view
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_seeker', 'is_employer')
    
    # This ensures you can edit is_seeker and is_employer on the user detail page
    fieldsets = UserAdmin.fieldsets + (
        ('User Roles', {'fields': ('is_seeker', 'is_employer')}),
    )

# Unregister the default User model (if it was registered) and register our CustomUserAdmin
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass 

# Register your custom User model with the custom Admin settings
admin.site.register(User, CustomUserAdmin) 


# 2. Admin for the Job Model
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'job_type', 'created_by', 'created_at')
    search_fields = ('title', 'company', 'location')
    list_filter = ('job_type', 'created_at', 'company')
    # Use 'created_by' field from your models.py
    ordering = ('-created_at',)


# 3. Admin for the Application Model
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    # Use helper functions to display related fields
    list_display = ('job', 'get_applicant_username', 'get_applicant_email', 'status', 'applied_at')
    search_fields = ('applicant__username', 'applicant__email', 'job__title') 
    list_filter = ('status', 'job', 'applied_at') 

    # Helper function to get applicant username
    def get_applicant_username(self, obj):
        return obj.applicant.username
    get_applicant_username.short_description = "Applicant Username" # Sets column header

    # Helper function to get applicant email
    def get_applicant_email(self, obj):
        return obj.applicant.email
    get_applicant_email.short_description = "Applicant Email" # Sets column header


# 4. Register Profile Models
admin.site.register(SeekerProfile)
admin.site.register(EmployerProfile)