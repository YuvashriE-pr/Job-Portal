from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Job, Application
from .models import SeekerProfile, EmployerProfile

class SeekerSignUpForm(UserCreationForm):
    class Meta:
        model  = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_seeker = True   # Mark as job seeker
        if commit:
            user.save()
        return user


class EmployerSignUpForm(UserCreationForm):
    class Meta:
        model  = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_employer = True   # Mark as employer
        if commit:
            user.save()
        return user


class JobForm(forms.ModelForm):
    class Meta:
        model  = Job
        exclude = ('created_by', 'created_at')   # Filled automatically
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class ApplicationForm(forms.ModelForm):
    class Meta:
        model  = Application
        fields = ('resume', 'cover_note')
        widgets = {
            'cover_note': forms.Textarea(attrs={'rows': 3}),
        }
class SeekerProfileForm(forms.ModelForm):
    class Meta:
        model = SeekerProfile
        fields = ('resume', 'skills', 'experience', 'education')

class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = EmployerProfile
        fields = ('company_name', 'company_description', 'website')