from django.urls import path
from . import views
from applications.views import apply_job

app_name = 'jobs'

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('job/<int:id>/', views.job_detail, name='job_detail'),
    path("delete-job/<int:job_id>/", views.delete_job, name="delete_job"),
    path("dashboard/", views.recruiter_dashboard, name="recruiter_dashboard"),
    path("applicants/<int:job_id>/", views.view_applicants, name="view_applicants"),
    path("create-job/", views.create_job, name="create_job"),
]
