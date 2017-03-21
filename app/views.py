"""
Definition of views.
"""
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from app.models import *
import logging

logger = logging.getLogger('django')

def get_unread_notifications(username):
    user = User.objects.get(username = username)
    unread_notifications = Notifications.objects.filter(receiver = user).filter(status = 'U')

    return unread_notifications

def _add_user_data_to_session(user, request):
    request.session['username'] = user.username
    request.session['first_name'] = user.first_name
    request.session['last_name'] = user.last_name
    request.session['full_name'] = user.first_name + ' ' + user.last_name
    request.session['email_id'] = user.email_id
    request.session['type'] = user.type

def login(request):
    assert isinstance(request, HttpRequest)

    if request.method == 'GET':
        return render(request, 'app/other/login.html', {'title':'Login',})
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username, password = password)
        
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                logger.info('User %s successfully authenticated' % username)
                next = ''

                if next in request.GET:
                    next = request.GET['next']
                if next is None or next == '':
                    user = User.objects.get(username = username)
                    _add_user_data_to_session(user, request)

                    if (user.type == 'S'):                        
                        next = reverse('student_home')
                    elif (user.type == 'G'):
                        next = reverse('guide_home')
                    elif (user.type == 'D'):
                        next = reverse('director_home')
                    elif (user.type == 'R'):
                        next = reverse('referee_home')

                return redirect(next)
            else:
                return redirect('403/')
        else:
            return redirect('403/')

@login_required
def logout(request):
    logger.info('User %s successfully logged out' % request.session['username'])
    auth.logout(request)

    return redirect('/')

def _get_notifications_for_user(username):
    notifications = Notifications.objects.filter(receiver = username)

    return notifications

@login_required
def user_edit_profile(request):
    assert isinstance(request, HttpRequest)
    
    if request.method == 'GET':
        user_details = User.objects.get(username = request.session['username'])

        return render(request, 'app/common/edit_profile.html', {
                'title':'Notifications',
                'descriptive_title' : 'All notifications',
                'user_details' : user_details
            })
    elif request.method == 'POST':
        user_name = request.session['username']
        user_details = User.objects.get(username = user_name)
        first_name = request.POST['first-name']
        last_name = request.POST['last-name']
        email_id = request.POST['email-id']
        address = request.POST['address']

        user_details.first_name = first_name
        user_details.last_name = last_name
        user_details.email_id = email_id
        user_details.address = address
        user_details.save() 

        return redirect(reverse('user_edit_profile'))

    return redirect(reverse('unauthorized_access'))

@login_required
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
    
    return (notification is not None) and (notification.receiver.username == username)

@login_required
def delete_user_notification(request, id):
    assert isinstance(request, HttpRequest)

    if request.method == "POST" and _verify_user_notification(request.session['username'], id):
        notification = Notifications.objects.get(id = id)
        notification.delete()

        return redirect(reverse('user_notifications'))
    else:
        return redirect(reverse('unauthorized_access'))

@login_required
def delete_all_unread_notifications(request):
    if request.method == "POST":
        user = User.objects.get(username = request.session['username'])
        notifications = Notifications.objects.filter(receiver = user).filter(status = 'U')
        notifications.delete()

        return redirect(reverse('user_notifications'))
    else:
        return redirect(reverse('unauthorized_access'))

@login_required
def delete_all_read_notifications(request):
    if request.method == "POST":
        user = User.objects.get(username = request.session['username'])
        notifications = Notifications.objects.filter(receiver = user).filter(status = 'R')
        notifications.delete()

        return redirect(reverse('user_notifications'))
    else:
        return redirect(reverse('unauthorized_access'))

@login_required
def mark_all_notifications_read(request):
    if request.method == "POST":
        user = User.objects.get(username = request.session['username'])
        notifications = Notifications.objects.filter(receiver = user).filter(status = 'U')

        for notification in notifications:
            notification.status = 'R'
            notification.save()

        return redirect(reverse('user_notifications'))
    else:
        return redirect(reverse('unauthorized_access'))

@login_required
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