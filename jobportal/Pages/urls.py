from django.urls import path
from . import views

app_name = 'Pages'

urlpatterns = [
    path('services/', views.services, name='services'),
    path('counselling/', views.counselling, name='counselling'),
    path('history', views.history, name='history'),
    path('contact/', views.contact, name='contact'),
    path('Skill_Assessment', views.Skill_Assessment,name='Skill_Assessment'),
    path('resume/create/', views.create_resume, name='create_resume'),
    path("resume/<int:id>/", views.resume_preview, name="resume_preview"),
    path("contact_mail/",views.contact_mail, name='contact_mail'),
    path('resume/download/<int:resume_id>/', views.download_resume, name='download_resume'),
    path('schedule_interview/',views.schedule_interview, name='schedule_interview'),
    # path('Add_assessment', views.Add_assessment , name="Add_assessment"),
    path("send_mail/", views.send_mail_view, name="send_mail"),
    path("candidate/", views.candidate, name="candidate"),
    path("candidate/<int:application_id>/", views.candidate_profile, name="candidate_profile"),
]
