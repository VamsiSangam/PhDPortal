from app.views import *

@login_required
def guide_home(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    return render(
        request,
        'app/guide/home.html',
        {
            'title':'Home Page',
            'descriptive_title' : 'Welcome ' + request.session['full_name'] + ' !',
            'unread_notifications' : get_unread_notifications(request.session['username'])
        }
    )

@login_required
def guide_edit_profile(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    return render(
        request,
        'app/guide/edit_profile.html',
        {
            'title':'Edit Profile',
            'descriptive_title' : 'Edit your profile',
            'unread_notifications' : get_unread_notifications(request.session['username'])
        }
    )

@login_required
def guide_view_student_info(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    return render(
        request,
        'app/guide/view_student_info.html',
        {
            'title':'Student Info',
            'descriptive_title' : 'View information about PhD students',
            'unread_notifications' : get_unread_notifications(request.session['username'])
        }
    )

@login_required
def guide_unevaulated_synopsis(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    return render(
        request,
        'app/guide/unevaluated_synopsis.html',
        {
            'title':'Unevaluated Synopsis',
            'descriptive_title' : 'View unevaluated synopsis sumitted by students',
            'unread_notifications' : get_unread_notifications(request.session['username'])
        }
    )

@login_required
def guide_archived_synopsis(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    return render(
        request,
        'app/guide/archived_synopsis.html',
        {
            'title':'Archived Synopsis',
            'descriptive_title' : 'View synopsis which were approved',
            'unread_notifications' : get_unread_notifications(request.session['username'])
        }
    )

@login_required
def guide_unevaluated_thesis(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    return render(
        request,
        'app/guide/unevaluated_thesis.html',
        {
            'title':'Unevaluated Thesis',
            'unread_notifications' : get_unread_notifications(request.session['username'])
        }
    )

@login_required
def guide_archived_thesis(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    return render(
        request,
        'app/guide/archived_thesis.html',
        {
            'title':'Archived Thesis',
            'descriptive_title' : 'View thesis which were completely approved',
            'unread_notifications' : get_unread_notifications(request.session['username'])
        }
    )

@login_required
def guide_phd_status(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    return render(
        request,
        'app/guide/phd_status.html',
        {
            'title':'PhD Status',
            'descriptive_title' : 'View the status of ongoing PhDs',
            'unread_notifications' : get_unread_notifications(request.session['username'])
        }
    )

@login_required
def guide_help_procedure(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    return render(
        request,
        'app/guide/procedure.html',
        {
            'title':'Procedure',
            'descriptive_title' : 'PhD Evaluation Procedure',
            'unread_notifications' : get_unread_notifications(request.session['username'])
        }
    )

@login_required
def guide_help_contacts(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    return render(
        request,
        'app/guide/help_contacts.html',
        {
            'title':'Help Contacts',
            'descriptive_title' : 'Contacts for critical issues',
            'unread_notifications' : get_unread_notifications(request.session['username'])
        }
    )