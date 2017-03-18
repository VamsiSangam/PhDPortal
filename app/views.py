"""
Definition of views.
"""

from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.template import RequestContext
from django.contrib import auth
from datetime import datetime
from app.models import *

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

def logout(request):
    auth.logout(request)

    return redirect('/')

# ====== ===== Student Views ===== ===== #

def student_home(request):
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/student/home.html',
        {
            'title':'Home Page',
            'descriptive_title' : 'Welcome ' + request.session['first_name'] + ' !',
        }
    )

def student_all_notifications(request):
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/student/notifications.html',
        {
            'title':'Notifications',
            'descriptive_title' : 'All notifications',
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

# ====== ===== Guide Views ===== ===== #

def guide_home(request):
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/guide/home.html',
        {
            'title':'Home Page',
            'descriptive_title' : 'Welcome ' + request.session['full_name'] + ' !',
        }
    )

def guide_all_notifications(request):
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/guide/notifications.html',
        {
            'title':'Notifications',
            'descriptive_title' : 'All Notifications',
        }
    )

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


# ====== ===== Director Views ===== ===== #

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

def director_all_notifications(request):
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/director/notifications.html',
        {
            'title':'Notifications',
            'descriptive_title' : 'All Notifications',
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

# ====== ===== Referee Views ===== ===== #

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

def referee_all_notifications(request):
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/referee/notifications.html',
        {
            'title':'Notifications',
            'descriptive_title' : 'All Notifications',
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