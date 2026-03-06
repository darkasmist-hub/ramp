from django.urls import path
from . import views
from applications.views import apply_job

app_name = 'jobs'

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('job/<int:id>/', views.job_detail, name='job_detail'),
    path("delete-job/<int:job_id>/", views.delete_job, name="delete_job"),
    path("close-job/<int:job_id>/", views.close_job, name="close_job"),
    path("dashboard/", views.recruiter_dashboard, name="recruiter_dashboard"),
    path("applicants/<int:job_id>/", views.view_applicants, name="view_applicants"),
    path("create-job/", views.create_job, name="create_job"),
    path("Jobseeker_dashboard/", views.Jobseeker_dashboard, name="Jobseeker_dashboard"),
    path("application/<int:app_id>/<str:status>/",views.update_application_status,name="update_application_status"),
    path("save/<int:job_id>/", views.save_job, name="save_job"),
    path("unsave/<int:job_id>/", views.unsave_job, name="unsave_job"),
    path("saved-jobs/", views.saved_jobs, name="saved_jobs"),
]
