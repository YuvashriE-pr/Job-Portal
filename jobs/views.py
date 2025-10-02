# jobs/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from .models import Job, Application, SeekerProfile, EmployerProfile, User
from .forms import ApplicationForm, SeekerSignUpForm, EmployerSignUpForm, JobForm, SeekerProfileForm, EmployerProfileForm

# ---------------------
# Home View
# ---------------------
def home(request):
    return render(request, 'jobs/home.html')

# ---------------------
# Job List View
# ---------------------
@login_required
def job_list(request):
    query = request.GET.get('q')
    job_type = request.GET.get('job_type')

    jobs = Job.objects.all()

    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) |
            Q(company__icontains=query) |
            Q(location__icontains=query) |
            Q(description__icontains=query)
        )
    
    if job_type:
        jobs = jobs.filter(job_type=job_type)

    return render(request, 'jobs/job_list.html', {'jobs': jobs, 'query': query, 'job_type': job_type})
# ---------------------
# Job Detail View
# ---------------------
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'jobs/job_detail.html', {'job': job})

# ---------------------
# Apply to Job View
# ---------------------
@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if hasattr(request.user, 'is_employer') and request.user.is_employer:
        messages.error(request, 'Employers cannot apply for jobs.')
        return render(request, 'jobs/apply.html', {'job': job})

    if Application.objects.filter(job=job, applicant=request.user).exists():
        messages.warning(request, 'You have already applied for this job.')
        return render(request, 'jobs/apply.html', {'job': job})

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.applicant = request.user
            application.job = job
            application.save()
            messages.success(request, 'Your application has been submitted successfully!') # <-- Add this line
            return redirect('job_detail', job_id=job.id)
    else:
        form = ApplicationForm()

    return render(request, 'jobs/apply.html', {'form': form, 'job': job})

# ---------------------
# Seeker Dashboard
# ---------------------
@login_required
def seeker_dashboard(request):
    apps = Application.objects.filter(applicant=request.user)
    return render(request, 'jobs/seeker_dashboard.html', {'apps': apps})

# ---------------------
# Employer Dashboard
# ---------------------
@login_required
def employer_dashboard(request):
    if not hasattr(request.user, 'is_employer') or not request.user.is_employer:
        return redirect('job_list')
    jobs = Job.objects.filter(created_by=request.user)
    return render(request, 'jobs/employer_dashboard.html', {'jobs': jobs})

# ---------------------
# Seeker Registration
# ---------------------
def seeker_register(request):
    if request.method == 'POST':
        form = SeekerSignUpForm(request.POST)
        if form.is_valid():
          user = form.save(commit=False)
          user.is_seeker = True
          user.save()
          messages.success(request, 'Registration successful. You can now sign in!')
        return redirect('login')
    else:
        form = SeekerSignUpForm()
    return render(request, 'jobs/register.html', {'form': form})
# ---------------------
# Employer Registration
# ---------------------
def employer_register(request):
    if request.method == 'POST':
        form = EmployerSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = EmployerSignUpForm()
    return render(request, 'jobs/register.html', {'form': form})

# ---------------------
# Post Job
# ---------------------
@login_required
def post_job(request):
    if not hasattr(request.user, 'is_employer') or not request.user.is_employer:
        return redirect('job_list')

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.created_by = request.user
            job.save()
            messages.success(request, 'Job posted successfully!')
            return redirect('employer_dashboard')
    else:
        form = JobForm()

    return render(request, 'jobs/post_job.html', {'form': form})

# ---------------------
# View Applications
# ---------------------
@login_required
def view_applications(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if job.created_by != request.user:
        return redirect('employer_dashboard')
    applications = Application.objects.filter(job=job)
    return render(request, 'jobs/view_applications.html', {'job': job, 'applications': applications})

# ---------------------
# edit
# ---------------------
@login_required
def edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if job.created_by != request.user:
        return redirect('employer_dashboard')

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated successfully!')
            return redirect('employer_dashboard')
    else:
        form = JobForm(instance=job)

    return render(request, 'jobs/edit_job.html', {'form': form, 'job': job})

# ---------------------
# delete
# ---------------------
@login_required
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if job.created_by != request.user:
        return redirect('employer_dashboard')

    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job deleted successfully!')
        return redirect('employer_dashboard')

    return render(request, 'jobs/confirm_delete.html', {'job': job})

# ---------------------
# Custom Logout
# ---------------------
class CustomLogoutView(LogoutView):
    http_method_names = ['get', 'post']
    next_page = 'job_list'

# ---------------------
# Consolidated Profile Views
# ---------------------
@login_required
def profile_view(request):
    if request.user.is_seeker:
        profile, created = SeekerProfile.objects.get_or_create(user=request.user)
        template_name = 'jobs/seeker_profile.html'
    elif request.user.is_employer:
        profile, created = EmployerProfile.objects.get_or_create(user=request.user)
        template_name = 'jobs/employer_profile.html'
    else:
        return redirect('job_list')

    return render(request, template_name, {'profile': profile})

@login_required
def profile_edit_view(request):
    if request.user.is_seeker:
        profile = request.user.seeker_profile
        form_class = SeekerProfileForm
        template_name = 'jobs/seeker_profile_edit.html'
    elif request.user.is_employer:
        profile = request.user.employer_profile
        form_class = EmployerProfileForm
        template_name = 'jobs/employer_profile_edit.html'
    else:
        return redirect('job_list')

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_view')
    else:
        form = form_class(instance=profile)

    return render(request, template_name, {'form': form})

@login_required
def delete_application(request, application_id):
    application = get_object_or_404(Application, id=application_id)

    # Check if the logged-in user is the one who submitted the application
    if application.applicant != request.user:
        messages.error(request, "You are not authorized to delete this application.")
        return redirect('seeker_dashboard')
    
    # Handle both GET and POST requests
    if request.method == 'POST':
        application.delete()
        messages.success(request, 'Your application has been deleted successfully.')
        return redirect('seeker_dashboard')
        
    return render(request, 'jobs/confirm_delete_application.html', {'application': application})

@login_required
def view_resume(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    if application.applicant != request.user:
        messages.error(request, 'You are not authorized to view this resume.')
        return redirect('seeker_dashboard')

    # This will serve the file directly
    return redirect(application.resume.url)