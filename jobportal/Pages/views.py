import re
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.shortcuts import get_object_or_404, render, HttpResponse, redirect
from django.template.loader import get_template
from .models import Resume
from xhtml2pdf import pisa
from .forms import ResumeForm
from .models import Contact as contactmodel 
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Contact
from django.contrib import messages
from .models import SkillAssessment


def services(request):
  return render(request, 'pages/services.html')

def counselling(request):
  return render(request, 'Pages/counselling.html')

def history(request):
  return render(request, 'Pages/history.html')

def contact(request):
  return render(request, 'Pages/contact.html')

def Skill_Assessment(request):
    return render(request, 'Pages/Skill_Assessment.html')


def format_bold(text):
    # convert **text** to <strong>text</strong>
    text = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", text)
    text = text.replace("\n", "<br>")
    return mark_safe(text)

@login_required
def create_resume(request):
    if request.method == "POST":
        form = ResumeForm(request.POST,request.FILES)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume = form.save()
            return redirect("Pages:resume_preview", resume.id)
    else:
        form = ResumeForm()

    return render(request, "resume/create_resume.html", {"form": form})

@login_required
def resume_view(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    return render(request, "resume/resume_view.html", {"resume": resume})    

@login_required
def resume_preview(request, id):
    resume = Resume.objects.get(id=id)

    formatted_experience = format_bold(resume.experience)
    formatted_education = format_bold(resume.education)

    return render(request, "resume/preview.html", {
        "resume": resume,
        "experience_html": formatted_experience,
        "education_html": formatted_education,
    })

@login_required
def download_resume(request, resume_id):
    resume = Resume.objects.get(id=resume_id, user=request.user)

    template_name = f"resume_Template/{resume.template}.html"
    template = get_template(template_name)
    html = template.render({'resume': resume})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        f'attachment; filename="{resume.full_name}_Resume.pdf"'
    )

    pisa.CreatePDF(html, dest=response)
    return response


def skill_assessment(request):
    score = None
    if request.method == "POST":
        answers = [
            request.POST.get("q1"),
            request.POST.get("q2"),
            request.POST.get("q3"),
        ]
        SkillAssessment.objects.create(
        user=request.user,
        score=score
    )

        correct_answers = ["python", "django", "html"]

        score = 0
        for i in range(len(correct_answers)):
            if answers[i] == correct_answers[i]:
                score += 1

    return render(request, "Pages/skill_assessment.html", {"score": score})

@login_required
def contact_mail(request):
    # Safety check
    print("VIEW HIT:", type(request), request.method) 
    if not hasattr(request, 'user') or not request.user.is_authenticated:
        return redirect('accounts:login')  # change 'login' to your login URL name

    if request.method == "POST":
        firstname = request.POST.get('First name', '').strip()
        lastname = request.POST.get('Last name', '').strip()
        Email = request.POST.get('Email', '').strip()
        Phone = request.POST.get('Phone number', '').strip()
        user_message = request.POST.get('Message', '').strip()

        # Safety check for empty fields
        if not all([firstname, lastname, Email, Phone, user_message]):
            return render(request, 'Pages/contact.html', {
                "status": "error",
                "error_message": "All fields are required."
            })

        Contact.objects.create(
            Email=Email,
            user=request.user,  # ✅ this will now always be a real User object
            firstname=firstname,
            lastname=lastname,
            Phone=Phone,
            message=user_message,
        )

        subject = "Your message has been received"
        email_body = f"Thank you for contacting us!\n\nYour message:\n{user_message}"
        from_email = "darkas.mist@gmail.com"

        send_mail(subject, email_body, from_email, [Email], fail_silently=False)
        
        messages.success(request, "Your message has been sent successfully!")

        return render(request, 'Pages/contact.html', {
            "status": "send_mail",
            "Email": Email
        })

    return render(request, 'Pages/contact.html')


from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def counselling(request):
    if request.method == "POST":
        # You can save data in DB here
        return render(request, "Pages/counselling.html", {
            "success": True
        })

    return render(request, "Pages/counselling.html")

# @login_required
# def send_mail(request):
#     if request.method == "POST":
#         Email = request.POST.get('Email')
        
#         message = request.POST.get(message)