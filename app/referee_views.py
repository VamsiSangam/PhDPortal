from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.template import RequestContext
from django.contrib import auth
from datetime import datetime
from app.models import *

def referee_home(request):
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/referee/home.html',
        {
            'title':'Home Page',
            'descriptive_title' : 'Welcome Prof. Chong Chang!',
        }
    )

def referee_edit_profile(request):
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/referee/edit_profile.html',
        {
            'title':'Edit Profile',
            'descriptive_title' : 'Edit your profile',
        }
    )

def referee_requestedlist(request):
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/referee/synopsis_list.html',
        {
            'title':'Synopsis Info',
            'descriptive_title' : 'View synopsis of requested',
        }
    )

def referee_evaluation(request):
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/referee/thesis_list.html',
        {
            'title':'Evaluate Thesis',
            'descriptive_title' : 'View the thesis along with feedback submission button',
        }
    )

def referee_evaluation_report(request):
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/referee/submit_final_feedback.html',
        {
            'title':'Submit final evaluated report',
            'descriptive_title' : 'feedback submission button',
        }
    )

def referee_help_procedure(request):
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/referee/procedure.html',
        {
            'title':'Procedure',
            'descriptive_title' : 'PhD Evaluation Procedure',
        }
    )

def referee_help_contacts(request):
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/referee/help_contacts.html',
        {
            'title':'Help Contacts',
            'descriptive_title' : 'Contacts for critical issues',
        }
    )