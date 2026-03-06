from django.core.paginator import Paginator
from django.shortcuts import render,get_object_or_404,redirect
from .models import Job,JobApplication
from jobs.models import JobApplication
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import JobForm
from django.utils import timezone
from .models import SavedJob
from django.contrib import messages
from django.http import HttpResponseForbidden

# from .models import Requirnment

def job_list(request):
    # jobs = Job.objects.all()
    jobs = Job.objects.filter(
        expires_at__gt=timezone.now(),
        status="open"
    )
    saved_jobs = SavedJob.objects.filter(user=request.user).values_list("job_id", flat=True)

    paginator = Paginator(jobs, 5)  # 5 jobs per page
    page_number = request.GET.get('page')
    jobs = paginator.get_page(page_number)

    return render(request, "jobs/jobs.html", {
        "jobs": jobs,
        "saved_jobs": saved_jobs
    })

def job_detail(request, id):
    job = get_object_or_404(Job, id=id)
    # requirment = get_object_or_404(Requirnment)  
    similar_jobs = Job.objects.filter(
        job_type=job.job_type
    ).exclude(id=job.id)[:5]
    return render(request, 'jobs/job_detail.html', {'job': job,'similar_jobs': similar_jobs})

@login_required
def recruiter_dashboard(request):
    jobs = Job.objects.filter(employer=request.user)
    total_jobs = jobs.count()
    total_applications = JobApplication.objects.filter(
    job__employer=request.user
).count()

    context = {
        "jobs": jobs,
        "total_jobs": total_jobs,
        "total_applications": total_applications,
    }

    return render(request, "jobs/recruiter_dashboard.html", context)


@login_required
def create_job(request):
    # if not request.user.is_recruiter:
    #     return HttpResponseForbidden("You are not allowed")
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user
            job.save()
            return redirect("jobs:recruiter_dashboard")
    else:
        form = JobForm()

    return render(request, "jobs/create_job.html", {"form": form})

@login_required
def update_application_status(request, app_id, status):

    application = get_object_or_404(JobApplication, id=app_id)

    # only job owner can change status
    if application.job.employer != request.user:
        return redirect("jobs:job_list")

    application.status = status
    application.save()

    return redirect("jobs:view_applicants", job_id=application.job.id)

def view_applicants(request, job_id):
    job = get_object_or_404(Job, id=job_id, employer=request.user)
    applications = job.applications.all()

    return render(request, "jobs/view_applicants.html", {
        "job": job,
        "applications": applications
    })
    
@login_required
def delete_job(request, job_id):

    job = get_object_or_404(Job, id=job_id, employer=request.user)
    job.delete()
    messages.success(request, "Job deleted successfully.")

    return redirect("jobs:recruiter_dashboard")

@login_required
def close_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, employer=request.user)
    job.status = "closed"
    job.save()

    return redirect("jobs:recruiter_dashboard")

@login_required
def Jobseeker_dashboard(request):

    applications = JobApplication.objects.filter(applicant=request.user)

    context = {
        "applied": applications.filter(status="applied"),
        "review": applications.filter(status="review"),
        "shortlisted": applications.filter(status="shortlisted"),
        "rejected": applications.filter(status="rejected"),
    }

    return render(request, "jobs/Jobseeker_dashboard.html", context)

@login_required
def save_job(request, job_id):

    job = get_object_or_404(Job, id=job_id)

    SavedJob.objects.get_or_create(
        user=request.user,
        job=job
    )
    return redirect(request.META.get("HTTP_REFERER"))

@login_required
def unsave_job(request, job_id):

    job = get_object_or_404(Job, id=job_id)

    SavedJob.objects.filter(
        user=request.user,
        job=job
    ).delete()

    return redirect(request.META.get("HTTP_REFERER"))

@login_required
def saved_jobs(request):
    saved_jobs = SavedJob.objects.filter(
        user=request.user
    ).select_related("job")

    return render(request, "jobs/saved_jobs.html", {
        "saved_jobs": saved_jobs
    })