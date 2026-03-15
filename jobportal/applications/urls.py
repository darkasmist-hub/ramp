from django.urls import path
from . import views

app_name = "applications"

urlpatterns = [
    path("apply/<int:job_id>/", views.apply_job, name="apply_job"),
    path("create-assessment/", views.create_assessment, name="create_assessment"),
    path("add-question/<int:template_id>/", views.add_question, name="add_question"),
]