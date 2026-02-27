from django.shortcuts import get_object_or_404, render, HttpResponse, redirect
from .models import Notification
from django.contrib.auth.decorators import login_required

# Create your views here.
def notifications(request):
  return render(request, 'notifications/notification.html')


# @login_required
# def notifications(request):
#     notifications = Notification.objects.filter(
#         user=request.user
#     ).order_by('-created_at')

#     return render(request, 'notifications/notification.html', {
#         'notifications': notifications
#     })
    
# @login_required
# def mark_notification_read(request, notification_id):
#     notification = Notification.objects.get(
#         id=notification_id,
#         user=request.user
#     )
#     notification.is_read = True
#     notification.save()
#     return redirect('notifications')

