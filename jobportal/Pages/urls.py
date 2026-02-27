from django.urls import path
from . import views

app_name = 'Pages'

urlpatterns = [
    path('services/', views.services, name='services'),
    path('counselling/', views.counselling, name='counselling'),
    path('history', views.history, name='history'),
    path('contact/', views.contact, name='contact'),
    path('skill_Assessment', views.Skill_Assessment,name='Skill_Assessment'),
    path('resume/create/', views.create_resume, name='create_resume'),
    path("resume/<int:id>/", views.resume_preview, name="resume_preview"),
    path("contact_mail/",views.contact_mail, name='contact_mail'),
    path('resume/download/<int:resume_id>/', views.download_resume, name='download_resume'),
]
