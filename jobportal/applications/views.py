from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from jobs.models import Job
from .models import Application


@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # Prevent provider from applying
    if request.user.profile.role != "seeker":
        return redirect("accounts:provider_dashboard")

    # Prevent duplicate applications
    already_applied = Application.objects.filter(user=request.user, job=job).exists()
    if already_applied:
        return redirect("jobs:job_detail", job_id=job.id)

    if request.method == "POST":
        cover_letter = request.POST.get("cover_letter")
        resume = request.FILES.get("resume")

        Application.objects.create(
            user=request.user,
            job=job,
            cover_letter=cover_letter,
            resume=resume,
        )

        return redirect("accounts:seeker_dashboard")

    return render(request, "applications/apply_job.html", {"job": job})