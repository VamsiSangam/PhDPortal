"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime

def login(request):
    """ Render's login page """
    assert isinstance(request, HttpRequest)

    if request.method == 'GET':
        return render(
            request,
            'app/other/login.html',
            {
                'title':'Login',
            }
        )
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

# ====== ===== Student Views ===== ===== #

def student_home(request):
    """Renders the student home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/student/home.html',
        {
            'title':'Home Page',
            'descriptive_title' : 'Welcome John Doe!',
            'user' : 'student',
        }
    )

def student_all_notifications(request):
    """Renders the all student notifications page"""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/student/notifications.html',
        {
            'title':'Notifications',
            'descriptive_title' : 'All notifications',
            'user' : 'student',
        }
    )

def student_edit_profile(request):
    """Renders student's edit profile page"""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/student/edit_profile.html',
        {
            'title':'Edit Profile',
            'descriptive_title' : 'Edit your profile',
            'user' : 'student',
        }
    )

def student_upload_synopsis(request):
    """Renders student's upload synopsis page"""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/student/upload_synopsis.html',
        {
            'title':'Upload Synopsis',
            'descriptive_title' : 'Upload Synopsis',
            'user' : 'student',
        }
    )

def student_view_synopsis(request):
    """Renders student's uploaded synopsis"""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/student/view_synopsis.html',
        {
            'title':'View Synopsis',
            'descriptive_title' : 'View you submitted synopsis',
            'user' : 'student',
        }
    )

def student_upload_thesis(request):
    """Renders student's upload thesis page"""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/student/upload_thesis.html',
        {
            'title':'Upload Thesis',
            'descriptive_title' : 'Upload PhD Thesis',
            'user' : 'student',
        }
    )

def student_view_thesis(request):
    """Renders student's uploaded thesis"""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/student/view_thesis.html',
        {
            'title':'View Thesis',
            'descriptive_title' : 'View you submitted PhD thesis',
            'user' : 'student',
        }
    )

def student_add_keywords(request):
    """Renders student's add/view keywords"""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/student/add_keywords.html',
        {
            'title':'Add Keywords',
            'descriptive_title' : 'Add keywords to your PhD thesis',
            'user' : 'student',
        }
    )

def student_phd_status(request):
    """Render's students's PhD status page"""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/student/phd_status.html',
        {
            'title':'PhD Thesis Submission Status',
            'descriptive_title' : 'PhD Thesis Submission Status',
            'user' : 'student',
        }
    )

def student_help_procedure(request):
    """Renders student's help page : procedure"""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/student/procedure.html',
        {
            'title':'Procedure',
            'descriptive_title' : 'Having doubts about the submission procedure?',
            'user' : 'student',
        }
    )

def student_help_contacts(request):
    """Renders student's help page : contacts"""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/student/help_contacts.html',
        {
            'title':'Help Contacts',
            'descriptive_title' : 'Contacts for critical issues',
            'user' : 'student',
        }
    )

# ====== ===== Guide Views ===== ===== #

def guide_home(request):
    """Renders guide's homepage"""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/guide/home.html',
        {
            'title':'Home Page',
            'descriptive_title' : 'Welcome Dr. Pavan Chakraborthy!',
            'user' : 'guide',
        }
    )

def guide_all_notifications(request):
    """Renders guide's all notifications page"""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/guide/notifications.html',
        {
            'title':'Notifications',
            'descriptive_title' : 'All Notifications',
            'user' : 'guide',
        }
    )

def guide_edit_profile(request):
    """Renders guide's edit profile page"""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/guide/edit_profile.html',
        {
            'title':'Edit Profile',
            'descriptive_title' : 'Edit your profile',
            'user' : 'guide',
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
            'user' : 'guide',
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
            'user' : 'guide',
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
            'user' : 'guide',
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
            'user' : 'guide',
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
            'user' : 'guide',
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
            'user' : 'guide',
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
            'user' : 'guide',
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
            'user' : 'guide',
        }
    )


# ====== ===== Director Views ===== ===== #

def director_home(request):
    """Renders director's homepage"""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/director/home.html',
        {
            'title':'Home Page',
            'descriptive_title' : 'Welcome Prof. G.C Nandi!',
            'user' : 'director',
        }
    )

def director_all_notifications(request):
    """Renders director's all notifications page"""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/director/notifications.html',
        {
            'title':'Notifications',
            'descriptive_title' : 'All Notifications',
            'user' : 'director',
        }
    )

def director_edit_profile(request):
    """Renders director's edit profile page"""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/director/edit_profile.html',
        {
            'title':'Edit Profile',
            'descriptive_title' : 'Edit your profile',
            'user' : 'director',
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
            'user' : 'director',
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
            'user' : 'director',
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
            'user' : 'director',
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
            'user' : 'director',
        }
    )

# ====== ===== Referee Views ===== ===== #

def referee_home(request):
    """Renders referee's homepage"""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/referee/home.html',
        {
            'title':'Home Page',
            'descriptive_title' : 'Welcome Prof. Chong Chang!',
            'user' : 'referee',
        }
    )

def referee_all_notifications(request):
    """Renders referee's all notifications page"""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/referee/notifications.html',
        {
            'title':'Notifications',
            'descriptive_title' : 'All Notifications',
            'user' : 'referee',
        }
    )

def referee_edit_profile(request):
    """Renders referee's edit profile page"""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/referee/edit_profile.html',
        {
            'title':'Edit Profile',
            'descriptive_title' : 'Edit your profile',
            'user' : 'referee',
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
            'user' : 'referee',
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
            'user' : 'referee',
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
            'user' : 'referee',
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
            'user' : 'referee',
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
            'user' : 'referee',
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