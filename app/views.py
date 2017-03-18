"""
Definition of views.
"""

from app.login_views import *
from app.student_views import *
from app.guide_views import *
from app.director_views import *
from app.referee_views import *
from django.http import HttpResponse

def _get_notifications_for_user(username):
    notifications = Notifications.objects.filter(username = username);

    return notifications

def user_notifications(request):
    assert isinstance(request, HttpRequest)

    notifications = _get_notifications_for_user(request.session['username'])
    read_notifications = notifications.filter(status = 'R')
    unread_notifications = notifications.filter(status = 'U')

    return render(
        request,
        'app/common/notifications.html',
        {
            'title':'Notifications',
            'descriptive_title' : 'All notifications',
            'read_notifications': read_notifications,
            'unread_notifications': unread_notifications,
        }
    )

def _verify_user_notification(username, id):
    notification = Notifications.objects.get(id = id)
    
    return (notification is not None) and (notification.username.username == username)

def delete_user_notification(request, id):
    assert isinstance(request, HttpRequest)

    if request.method == "POST" and _verify_user_notification(request.session['username'], id):
        notification = Notifications.objects.get(id = id)
        notification.delete()

        return redirect(reverse('user_notifications'))
    else:
        return redirect(reverse('unauthorized_access'))

def delete_all_unread_notifications(request):
    if request.method == "POST":
        user = User.objects.get(username = request.session['username'])
        notifications = Notifications.objects.filter(username = user).filter(status = 'U')
        notifications.delete()

        return redirect(reverse('user_notifications'))
    else:
        return redirect(reverse('unauthorized_access'))

def delete_all_read_notifications(request):
    if request.method == "POST":
        user = User.objects.get(username = request.session['username'])
        notifications = Notifications.objects.filter(username = user).filter(status = 'R')
        notifications.delete()

        return redirect(reverse('user_notifications'))
    else:
        return redirect(reverse('unauthorized_access'))

def mark_all_notifications_read(request):
    if request.method == "POST":
        user = User.objects.get(username = request.session['username'])
        notifications = Notifications.objects.filter(username = user).filter(status = 'U')

        for notification in notifications:
            notification.status = 'R'
            notification.save()

        return redirect(reverse('user_notifications'))
    else:
        return redirect(reverse('unauthorized_access'))

def mark_notification_read(request, id):
    assert isinstance(request, HttpRequest)

    if request.method == "POST" and _verify_user_notification(request.session['username'], id):
        notification = Notifications.objects.get(id = id)
        notification.status = 'R'
        notification.save()

        return redirect(reverse('user_notifications'))
    else:
        return redirect(reverse('unauthorized_access'))

def resource_not_found(request):
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/other/404.html',
        {
            'title':'Resource not found'
        }
    )

def unauthorized_access(request):
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/other/403.html',
        {
            'title':'Resource not found'
        }
    )