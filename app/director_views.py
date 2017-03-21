from app.views import *

@login_required
def director_home(request):
    assert isinstance(request, HttpRequest)

    unread_notifications = get_unread_notifications(request.session['username'])

    return render(
        request,
        'app/director/home.html',
        {
            'title':'Home Page',
            'descriptive_title' : 'Welcome ' + request.session['full_name'] + ' !',
            'unread_notifications' : unread_notifications,
        }
    )

@login_required
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

@login_required
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

@login_required
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

@login_required
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

@login_required
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