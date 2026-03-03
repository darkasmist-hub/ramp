from django.core.paginator import Paginator
from django.shortcuts import render,get_object_or_404,redirect
from .models import Job,JobApplication
from applications.models import Application
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import JobForm
from django.utils import timezone
from django.http import HttpResponseForbidden
# from .models import Requirnment

def job_list(request):
    # jobs = Job.objects.all()
    jobs = Job.objects.filter(
        expires_at__gt=timezone.now()
    )
    paginator = Paginator(jobs, 5)  # 5 jobs per page
    page_number = request.GET.get('page')
    jobs = paginator.get_page(page_number)

    return render(request, 'jobs/jobs.html', {'jobs': jobs})

def job_detail(request, id):
    job = get_object_or_404(Job, id=id)
    # requirment = get_object_or_404(Requirnment)  
    similar_jobs = Job.objects.filter(
        job_type=job.job_type
    ).exclude(id=job.id)[:5]
    return render(request, 'jobs/job_detail.html', {'job': job,'similar_jobs': similar_jobs})


@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    send_mail(
        subject=f"New Application for {job.title}",
        message=f"A user applied for {job.title}",
        from_email="darkas.mist@gmail.com",
        recipient_list={job.companyEmail},
        fail_silently=False,
    )
    
    if request.method == "POST":
        resume = request.FILES.get("resume")
        JobApplication.objects.create(
            job=job,
            applicant=request.user,
            resume=resume,
        )
        return redirect("job_list")
    
    return render(request, "jobs/job_detail.html", {"job": job})

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


def view_applicants(request, job_id):
    job = get_object_or_404(Job, id=job_id, employer=request.user)
    applications = job.applications.all()

    return render(request, "jobs/view_applicants.html", {
        "job": job,
        "applications": applications
    })