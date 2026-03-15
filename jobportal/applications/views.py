from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from jobs.models import Job
from jobs.models import JobApplication
from django.core.mail import send_mail
from .forms import JobApplicationForm
from django.contrib import messages
from .models import AssessmentTemplate
from .models import Question, Option


@login_required
def apply_job(request, job_id):

    job = get_object_or_404(Job, id=job_id)
    if request.user.profile.role != "seeker":
        return redirect("accounts:provider_dashboard")

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
    

@login_required
def create_assessment(request):

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        duration = request.POST.get("duration")

        template = AssessmentTemplate.objects.create(
            title=title,
            description=description,
            duration=duration,
            created_by=request.user
        )
        return redirect("applications:add_question", template.id)

    return render(request, "applications/create_assessment.html")



@login_required
def add_question(request, template_id):

    assessment = AssessmentTemplate.objects.get(id=template_id)

    if request.method == "POST":
        question_text = request.POST.get("question")
        options = request.POST.getlist("options")
        correct_option = request.POST.get("correct_option")

        question = Question.objects.create(
            assessment=assessment,
            text=question_text,
            correct_option=correct_option
        )
        for opt in options:
            Option.objects.create(question=question, text=opt)

        action = request.POST.get("action")
        if action == "add_more":
            return redirect("applications:add_question", template_id)
        return redirect("applications:create_assessment", assessment.job.id)

    return render(request, "applications/add_question.html", {
        "assessment": assessment
    })