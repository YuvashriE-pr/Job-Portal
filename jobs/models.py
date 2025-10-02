from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
# -----------------------
# Custom User Model
# -----------------------
class User(AbstractUser):
    is_employer = models.BooleanField(default=False)
    is_seeker = models.BooleanField(default=False)

    def __str__(self):
        return self.username

# -----------------------
# Job Model
# -----------------------
class Job(models.Model):
    JOB_TYPES = [
        ('Full-Time', 'Full-Time'),
        ('Part-Time', 'Part-Time'),
        ('Remote', 'Remote'),
        ('Internship', 'Internship'),
    ]
    title       = models.CharField(max_length=200)
    company     = models.CharField(max_length=150)
    location    = models.CharField(max_length=120)
    job_type    = models.CharField(max_length=20, choices=JOB_TYPES)
    description = models.TextField()
    deadline    = models.DateField()
    created_by  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs')
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} @ {self.company}"

# -----------------------
# Job Application Model
# -----------------------
class Application(models.Model):
    STATUS = [
        ('applied','Applied'),
        ('review','In Review'),
        ('rejected','Rejected'),
        ('accepted','Accepted')
    ]
    job        = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    resume     = models.FileField(upload_to='resumes/')
    cover_note = models.TextField(blank=True)
    status     = models.CharField(max_length=10, choices=STATUS, default='applied')
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('job','applicant')

    def __str__(self):
        return f"{self.applicant} -> {self.job}"

# -----------------------
# Seeker Profile
# -----------------------
class SeekerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="seeker_profile")
    skills = models.TextField(blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    
    # These are the fields your form is looking for
    experience = models.TextField(blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} - Seeker Profile"

# -----------------------
# Employer Profile
# -----------------------
class EmployerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="employer_profile")
    company_name = models.CharField(max_length=255, blank=True, null=True)
    company_description = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - Employer Profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_seeker:
            SeekerProfile.objects.create(user=instance)
        elif instance.is_employer:
            EmployerProfile.objects.create(user=instance)

# This is a good practice to ensure the signal is connected
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'seeker_profile'):
        instance.seeker_profile.save()
    if hasattr(instance, 'employer_profile'):
        instance.employer_profile.save()
