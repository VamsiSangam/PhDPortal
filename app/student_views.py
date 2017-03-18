from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.template import RequestContext
from django.contrib import auth
from datetime import datetime
from app.models import *

def _get_unread_notifications(username):
    user = User.objects.get(username = username)
    unread_notifications = Notifications.objects.filter(username = user).filter(status = 'U')

    return unread_notifications

def student_home(request):
    assert isinstance(request, HttpRequest)
    
    unread_notifications = _get_unread_notifications(request.session['username'])

    return render(
        request,
        'app/student/home.html',
        {
            'title':'Home Page',
            'descriptive_title' : 'Welcome ' + request.session['first_name'] + ' !',
            'unread_notifications' : unread_notifications,
        }
    )

def student_edit_profile(request):
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/student/edit_profile.html',
        {
            'title':'Edit Profile',
            'descriptive_title' : 'Edit your profile',
        }
    )

def student_upload_synopsis(request):
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/student/upload_synopsis.html',
        {
            'title':'Upload Synopsis',
            'descriptive_title' : 'Upload Synopsis',
        }
    )

def student_view_synopsis(request):
    assert isinstance(request, HttpRequest)
    
    return render(
        request,
        'app/student/view_synopsis.html',
        {
            'title':'View Synopsis',
            'descriptive_title' : 'View you submitted synopsis',
        }
    )

def student_upload_thesis(request):
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/student/upload_thesis.html',
        {
            'title':'Upload Thesis',
            'descriptive_title' : 'Upload PhD Thesis',
        }
    )

def student_view_thesis(request):
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/student/view_thesis.html',
        {
            'title':'View Thesis',
            'descriptive_title' : 'View you submitted PhD thesis',
        }
    )

def student_add_keywords(request):
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/student/add_keywords.html',
        {
            'title':'Add Keywords',
            'descriptive_title' : 'Add keywords to your PhD thesis',
        }
    )

def student_phd_status(request):
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/student/phd_status.html',
        {
            'title':'PhD Thesis Submission Status',
            'descriptive_title' : 'PhD Thesis Submission Status',
        }
    )

def student_help_procedure(request):
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/student/procedure.html',
        {
            'title':'Procedure',
            'descriptive_title' : 'Having doubts about the submission procedure?',
        }
    )

def student_help_contacts(request):
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/student/help_contacts.html',
        {
            'title':'Help Contacts',
            'descriptive_title' : 'Contacts for critical issues',
        }
    )