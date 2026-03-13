from django.shortcuts import get_object_or_404, render, HttpResponse, redirect
from .models import Notification
from django.contrib.auth.decorators import login_required

# Create your views here.
# def notifications(request):
#   return render(request, 'notifications/notification.html')


@login_required
def notifications(request):

    notifications = Notification.objects.filter(
        user=request.user
    ).order_by("-created_at")
    return render(request, "notifications/Notification.html", {
        "notifications": notifications
    })
    
@login_required
def clear_notifications(request):

    Notification.objects.filter(user=request.user).delete()

    return redirect("notifications:notifications")
