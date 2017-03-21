from app.views import *

@login_required
def director_home(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    return render(
        request,
        'app/director/home.html',
        {
            'title':'Home Page',
            'descriptive_title' : 'Welcome ' + request.session['full_name'] + ' !',
            'unread_notifications' : get_unread_notifications(request.session['username'])
        }
    )

@login_required
def director_edit_profile(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    return render(
        request,
        'app/director/edit_profile.html',
        {
            'title':'Edit Profile',
            'descriptive_title' : 'Edit your profile',
            'unread_notifications' : get_unread_notifications(request.session['username'])
        }
    )

@login_required
def director_view_student_info(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    return render(
        request,
        'app/director/view_student_info.html',
        {
            'title':'Student Info',
            'descriptive_title' : 'View information about PhD students',
            'unread_notifications' : get_unread_notifications(request.session['username'])
        }
    )

@login_required
def director_submit_for_evaluation(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    return render(
        request,
        'app/director/submit_for_evaluation.html',
        {
            'title':'Shortlisting panel',
            'descriptive_title' : 'View and shortlist Panel Sent by Guide For Final evaluation',
            'unread_notifications' : get_unread_notifications(request.session['username'])
        }
    )

@login_required
def director_help_procedure(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    return render(
        request,
        'app/director/procedure.html',
        {
            'title':'Procedure',
            'descriptive_title' : 'PhD Evaluation Procedure',
            'unread_notifications' : get_unread_notifications(request.session['username'])
        }
    )

@login_required
def director_help_contacts(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    return render(
        request,
        'app/director/help_contacts.html',
        {
            'title':'Help Contacts',
            'descriptive_title' : 'Contacts for critical issues',
            'unread_notifications' : get_unread_notifications(request.session['username'])
        }
    )