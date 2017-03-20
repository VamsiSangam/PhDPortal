from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.template import RequestContext
from django.contrib import auth
from datetime import datetime
from app.models import *
from django.contrib.auth.decorators import login_required
from app.student_views import get_unread_notifications
import logging

logger = logging.getLogger('django')

@login_required
def guide_home(request):
    assert isinstance(request, HttpRequest)

    unread_notifications = get_unread_notifications(request.session['username'])

    return render(
        request,
        'app/guide/home.html',
        {
            'title':'Home Page',
            'descriptive_title' : 'Welcome ' + request.session['full_name'] + ' !',
            'unread_notifications' : unread_notifications,
        }
    )

@login_required
def guide_edit_profile(request):
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/guide/edit_profile.html',
        {
            'title':'Edit Profile',
            'descriptive_title' : 'Edit your profile',
        }
    )

@login_required
def guide_view_student_info(request):
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/guide/view_student_info.html',
        {
            'title':'Student Info',
            'descriptive_title' : 'View information about PhD students',
        }
    )

@login_required
def guide_unevaulated_synopsis(request):
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/guide/unevaluated_synopsis.html',
        {
            'title':'Unevaluated Synopsis',
            'descriptive_title' : 'View unevaluated synopsis sumitted by students',
        }
    )

@login_required
def guide_archived_synopsis(request):
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/guide/archived_synopsis.html',
        {
            'title':'Archived Synopsis',
            'descriptive_title' : 'View synopsis which were approved',
        }
    )

@login_required
def guide_unevaluated_thesis(request):
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/guide/unevaluated_thesis.html',
        {
            'title':'Unevaluated Thesis',
            'descriptive_title' : 'View unevaluated thesis sumitted by students',
        }
    )

@login_required
def guide_archived_thesis(request):
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/guide/archived_thesis.html',
        {
            'title':'Archived Thesis',
            'descriptive_title' : 'View thesis which were completely approved',
        }
    )

@login_required
def guide_phd_status(request):
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/guide/phd_status.html',
        {
            'title':'PhD Status',
            'descriptive_title' : 'View the status of ongoing PhDs',
        }
    )

@login_required
def guide_help_procedure(request):
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/guide/procedure.html',
        {
            'title':'Procedure',
            'descriptive_title' : 'PhD Evaluation Procedure',
        }
    )

@login_required
def guide_help_contacts(request):
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/guide/help_contacts.html',
        {
            'title':'Help Contacts',
            'descriptive_title' : 'Contacts for critical issues',
        }
    )