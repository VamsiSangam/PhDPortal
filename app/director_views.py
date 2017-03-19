from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.template import RequestContext
from django.contrib import auth
from datetime import datetime
from app.models import *

def director_home(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/director/home.html',
        {
            'title':'Home Page',
            'descriptive_title' : 'Welcome Prof. G.C Nandi!',
        }
    )

def director_edit_profile(request):
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/director/edit_profile.html',
        {
            'title':'Edit Profile',
            'descriptive_title' : 'Edit your profile',
        }
    )

def director_view_student_info(request):
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/director/view_student_info.html',
        {
            'title':'Student Info',
            'descriptive_title' : 'View information about PhD students',
        }
    )

def director_submit_for_evaluation(request):
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/director/submit_for_evaluation.html',
        {
            'title':'Shortlisting panel',
            'descriptive_title' : 'View and shortlist Panel Sent by Guide For Final evaluation',
        }
    )


def director_help_procedure(request):
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/director/procedure.html',
        {
            'title':'Procedure',
            'descriptive_title' : 'PhD Evaluation Procedure',
        }
    )

def director_help_contacts(request):
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/director/help_contacts.html',
        {
            'title':'Help Contacts',
            'descriptive_title' : 'Contacts for critical issues',
        }
    )