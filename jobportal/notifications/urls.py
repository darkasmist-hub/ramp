from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
   path('', views.notifications, name='list'),
   path("notifications/", views.notifications, name="notifications"),
   path("notifications/clear/", views.clear_notifications,name="clear_notifications"),
]
