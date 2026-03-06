from django.contrib import admin

# Register your models here.
from .models import Job
# from .models import Requirnment
from jobs.models import JobApplication

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'applicant', 'applied_at')

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company_name', 'location', 'job_type', 'salary')
    search_fields = ('title', 'company_name', 'location')
    list_filter = ('job_type', 'location')
    
# @admin.register(Requirnment)
# class RequirnmentAdmin(admin.ModelAdmin):
#     list_display = ('experience', 'education','skills', 'shift')