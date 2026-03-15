from django.contrib import admin
from django.urls import path
from accounts import views

app_name = 'accounts'

urlpatterns = [
  path('', views.home, name='home'),
  path("sign/", views.sign, name="sign"),
  path("send-otp/", views.send_otp_view, name="send_otp"),
  path("verify-otp/", views.verify_otp_view, name="verify_otp"),
  path("dashboard/", views.dashboard, name="dashboard"),
  path("logout/", views.user_logout, name="logout"),
  path("login/", views.user_login, name="user_login"),
  path("dashboard/seeker/", views.seeker_dashboard, name="seeker_dashboard"),
  path("dashboard/provider/", views.provider_dashboard, name="provider_dashboard"),
  path("create-profile/", views.create_profile, name="create_profile"),
  path("edit-profile/", views.edit_profile, name="edit_profile"), 
]

# urlpatterns = [
#     path('', views.home, name='home'),
#     path('sign/', views.sign, name='sign'),
#     path('login/', views.user_login, name='login'),
#     path('logout/', views.user_logout, name='logout'),
#     path('dashboard/', views.dashboard, name='dashboard'),
#     path('dashboard/seeker/', views.seeker_dashboard, name='seeker_dashboard'),
#     path('dashboard/provider/', views.provider_dashboard, name='provider_dashboard'),
#     path('send-otp/', views.send_otp_view, name='send_otp'),
#     path('verify-otp/', views.verify_otp_view, name='verify_otp'),
# ]