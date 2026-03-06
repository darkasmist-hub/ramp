from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from jobs.models import Job
from jobs.models import JobApplication
from django.core.mail import send_mail
from .forms import JobApplicationForm
from django.contrib import messages

# @login_required
# def apply_job(request, job_id):
#     job = get_object_or_404(Job, id=job_id)

#     # Prevent provider from applying
#     if request.user.profile.role != "seeker":
#         return redirect("accounts:provider_dashboard")

#     # Prevent duplicate applications
#     already_applied = JobApplication.objects.filter(applicant=request.user, job=job).exists()
#     if already_applied:
#         messages.warning(request, "You already applied for this job")
#         return redirect("jobs:job_detail", job_id=job.id)
    

#     if request.method == "POST":
#         cover_letter = request.POST.get("cover_letter")
#         resume = request.FILES.get("resume")

#         JobApplication.objects.create(
#             job=job,
#             applicant=request.user,
#             resume=resume,
#         )
#         send_mail(
#         subject=f"New Application for {job.title}",
#         message=f"A user applied for {job.title}",
#         from_email="darkas.mist@gmail.com",
#         recipient_list=[job.companyEmail],
#         fail_silently=False,
#         )

#         # return redirect("job_list")
#         messages.success(request, "Your Application has been sent to HR, keep track of your Application")
#         return redirect("jobs:job_detail", id=job.id)

#     return render(request, "applications/apply_job.html", {"job": job})

@login_required
def apply_job(request, job_id):

    job = get_object_or_404(Job, id=job_id)
    
    # Prevent provider/recruiter from applying
    if request.user.profile.role != "seeker":
        return redirect("accounts:provider_dashboard")

    # Prevent duplicate applications
    already_applied = JobApplication.objects.filter(
        applicant=request.user,
        job=job
    ).exists()

    if already_applied:
        messages.warning(request, "You already applied for this job")
        return redirect("jobs:job_detail", job_id=job.id)
    
    if job.status == "closed":
        messages.warning(request, "This job is no longer accepting applications")
        return redirect("jobs:job_detail", job_id=job.id)

    if request.method == "POST":
        form = JobApplicationForm(request.POST, request.FILES)

        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()

            messages.success(request, "Application submitted successfully")

            return redirect("jobs:job_detail", id=job.id)

    else:
        form = JobApplicationForm()

    return render(request, "applications/apply_job.html", {
        "form": form,
        "job": job
    })