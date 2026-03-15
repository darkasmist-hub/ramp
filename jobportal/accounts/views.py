from django.contrib.auth import login
from django.shortcuts import get_object_or_404, render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
import random
from django.contrib.auth import logout
from .models import OTPStorage
from django.core.mail import send_mail
from django.http import JsonResponse
from datetime import datetime
from django.utils.timezone import now
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from jobs.models import Job
from django.contrib.auth import authenticate
from django.urls import reverse
from django.contrib import messages
from jobs.models import JobApplication
from .models import CandidateProfile

def sign(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        role = request.POST.get('role')
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("accounts:sign")
        request.session['signup_data'] = {
            'username': username,
            'email': email,
            'password': password,
            'role': role,
        }
        return JsonResponse({"status": "send_otp", "email": email})
    return render(request, 'accounts/sign.html')

def home(request):
    return render(request, 'home.html')

# def sign(request): 
#     if request.method == "POST":
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         confirm_password = request.POST.get('confirm_password')
        
#         if password != confirm_password:
#           return JsonResponse({"error": "Passwords do not match"})
#             # messages.error(request, "Passwords do not match.")
#             # return render(request, 'sign.html', {'is_signup': True})
          
#         SignModel.objects.create(
#             username=username, 
#             email=email, 
#             password=make_password(password),
#         )
#         return JsonResponse({"status": "send_otp", "email": email})


#     return render(request, 'accounts/sign.html')
#     # return JsonResponse({"error": "Invalid request"})

def send_otp_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        if not email:
            return JsonResponse({"error": "Email is required"}, status=400)
        
        record = OTPStorage.objects.filter(email=email).first()
        
        if record and now() - record.created_at < timedelta(seconds=60):
            return JsonResponse({"error": "Please wait before requesting OTP"}, status=429)
        otp = str(random.randint(100000, 999999))
        
        OTPStorage.objects.update_or_create(email=email, defaults={'otp_code': otp})
        
        print("OTP GENERATED:", otp)
        # 3. Send Email
        subject = "Your OTP Code"
        message = f"Hello, Your login OTP is: {otp}"
        from_email = "darkas.mist@gmail.com"
        
        send_mail(subject, message, from_email, [email],fail_silently=False)
        
        return JsonResponse({"status":"otp_sent"})
    
    return JsonResponse({"error": "Invalid request"}, status=400)

# def verify_otp_view(request):
#     if request.method == "POST":
#         user_otp = request.POST.get('otp')
#         email = request.POST.get('email')
        
#         try:
#             record = OTPStorage.objects.get(email=email, otp_code=user_otp)
#             if now() - record.created_at > timedelta(minutes=5):
#               record.delete() 
#               return JsonResponse({"error":"OTP expired"})

#             record.delete() 
#             return JsonResponse({"success":True})

#         except OTPStorage.DoesNotExist:
#             return JsonResponse({"error":"OTP invalid"})
#     return JsonResponse({"error":"invalid request"})
  


def verify_otp_view(request):
    if request.method == "POST":
        user_otp = request.POST.get('otp')
        email = request.POST.get('email')

        try:
            record = OTPStorage.objects.get(email=email, otp_code=user_otp)

            signup_data = request.session.get('signup_data')
            username=signup_data['username'],
            email=signup_data['email'],
            password=signup_data['password']
            
            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
            else:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )

            user.profile.role = signup_data['role']
            user.profile.save()

            login(request, user)

            record.delete()
            del request.session['signup_data']

            if user.profile.role == "seeker":
                return JsonResponse({ "success": True, "redirect": reverse("accounts:seeker_dashboard")})
            elif user.profile.role == "provider":
                return JsonResponse({"success": True, "redirect": reverse("accounts:provider_dashboard")})
            else:
                return JsonResponse({"success": True, "redirect": reverse("accounts:home")})
                
        except OTPStorage.DoesNotExist:
            return JsonResponse({"error": "Invalid OTP"})

def user_login(request):
    if request.user.is_authenticated:
        return redirect("accounts:seeker_dashboard")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Handle ?next=
            next_url = request.GET.get("next")
            if next_url:
                return redirect(next_url)
            # Role-based redirect
            if user.profile.role == "seeker":
                return redirect("accounts:seeker_dashboard")
            else:
                return redirect("accounts:provider_dashboard")

        else:
            return render(request, "accounts/login.html", {
                "error": "Invalid username or password"
            })

    return render(request, "accounts/login.html")


@login_required
def dashboard(request):
    if request.user.profile.role == 'seeker':
        return redirect('accounts:seeker_dashboard')
    else:
        return redirect('accounts:provider_dashboard')

@login_required
def seeker_dashboard(request):

    # applications = JobApplication.objects.filter(applicant=request.user)

    # context = {
    #     "applied": applications.filter(status="applied"),
    #     "review": applications.filter(status="review"),
    #     "shortlisted": applications.filter(status="shortlisted"),
    #     "rejected": applications.filter(status="rejected"),
    # }

    return render(request, "accounts/seeker_dashboard.html",)

@login_required
def provider_dashboard(request):
    return render(request, 'accounts/provider_dashboard.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('accounts:home')


@login_required
def create_profile(request):

    profile = CandidateProfile.objects.filter(user=request.user).first()
    if profile:
        return redirect("accounts:edit_profile")
    
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        age = request.POST.get("age")
        dob = request.POST.get("dob")
        mobile = request.POST.get("mobile")
        job_preference = request.POST.get("job_preference")
        skills = request.POST.get("skills")
        profile_pic = request.FILES.get("profile_pic")
        resume = request.FILES.get("resume")
        location = request.POST.get("location")


        # Check if any field is empty
        if not all([full_name, age, dob, mobile, job_preference, skills, profile_pic]):
            return render(request, "accounts/create_profile.html", {
                "error": "All fields are required"
            })

        CandidateProfile.objects.create(
            user=request.user,
            full_name=full_name,
            age=int(age),
            dob=dob,
            mobile=mobile,
            job_preference=job_preference,
            skills=skills,
            profile_pic=profile_pic,
            resume=resume,
            location=location,
        )
        return redirect("accounts:home")

    return render(request, "accounts/create_profile.html")


@login_required
def edit_profile(request):
    profile = CandidateProfile.objects.get(user=request.user)
    if request.method == "POST":
        profile.full_name = request.POST.get("full_name")
        profile.age = request.POST.get("age")
        profile.dob = request.POST.get("dob")
        profile.mobile = request.POST.get("mobile")
        profile.job_preference = request.POST.get("job_preference")
        profile.skills = request.POST.get("skills")

        profile.location = request.POST.get("location")
        
        if request.FILES.get("profile_pic"):
            profile.profile_pic = request.FILES.get("profile_pic")

        if request.FILES.get("resume"):
            profile.resume = request.FILES.get("resume")


        profile.save()
        return redirect("accounts:dashboard")
    return render(request, "accounts/edit_profile.html", {"profile": profile})
