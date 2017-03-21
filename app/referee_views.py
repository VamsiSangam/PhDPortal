from app.views import *

@login_required
def referee_home(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    return render(
        request,
        'app/referee/home.html',
        {
            'title':'Home Page',
            'descriptive_title' : 'Welcome Prof. Chong Chang!',
            'unread_notifications' : get_unread_notifications(request.session['username']),
        }
    )

@login_required
def referee_requestedlist(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    return render(
        request,
        'app/referee/synopsis_list.html',
        {
            'title':'Synopsis Info',
            'descriptive_title' : 'View synopsis of requested',
            'unread_notifications' : get_unread_notifications(request.session['username']),
        }
    )

@login_required
def referee_evaluation(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    return render(
        request,
        'app/referee/thesis_list.html',
        {
            'title':'Evaluate Thesis',
            'descriptive_title' : 'View the thesis along with feedback submission button',
            'unread_notifications' : get_unread_notifications(request.session['username']),
        }
    )

@login_required
def referee_evaluation_report(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    return render(
        request,
        'app/referee/submit_final_feedback.html',
        {
            'title':'Submit final evaluated report',
            'descriptive_title' : 'feedback submission button',
            'unread_notifications' : get_unread_notifications(request.session['username']),
        }
    )

@login_required
def referee_help_procedure(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    return render(
        request,
        'app/referee/procedure.html',
        {
            'title':'Procedure',
            'descriptive_title' : 'PhD Evaluation Procedure',
            'unread_notifications' : get_unread_notifications(request.session['username']),
        }
    )

@login_required
def referee_help_contacts(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    return render(
        request,
        'app/referee/help_contacts.html',
        {
            'title':'Help Contacts',
            'unread_notifications' : get_unread_notifications(request.session['username']),
        }
    )