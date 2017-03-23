from app.views import *

@login_required
def guide_unevaluated_abstract(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))
    
    user = User.objects.get(username = request.session['username'])

    if request.method == "GET":
        # query for all the thesis under this guide which
        # whose abstract was not evaluated by this guide
        
        all_thesis = []     # list of dict

        # each element of all_thesis is a dict
        # dict['title'] = phd title
        # dict['student_full_name'] = student full name
        # dict['abstract'] = phd abstract
        # dict['student_username'] = student_username
        # dict['id'] = thesis_id (int)

        return render(
            request,
            'app/guide/unevaluated_abstract.html',
            {
                'title':'Unevaluated PhD Abstract',
                'descriptive_title' : 'View unevaluated abstracts sumitted by PhD students',
                'unread_notifications' : get_unread_notifications(request.session['username']),
                'all_thesis' : all_thesis
            }
        )
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def guide_evaluate_unevaluated_abstract(request):
    if request.method == "POST":
        # read post data
        # request.POST['id'] = string - thesis id
        # request.POST['isApproved'] = 'true' / 'false'
        # request.POST['feedback'] = feedback string
        # if true add row into ThesisGuideApprovals, with type = 'A'
        # if false remove all approvals for this thesis abstract so far
        # send notifications accordingly

        return HttpResponse('0', content_type = 'text/plain')
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def guide_unevaulated_synopsis(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    if request.method == "GET":
        return render(
            request,
            'app/guide/unevaluated_synopsis.html',
            {
                'title':'Unevaluated Synopsis',
                'descriptive_title' : 'View unevaluated synopsis sumitted by students',
                'unread_notifications' : get_unread_notifications(request.session['username'])
            }
        )
    else:
        return redirect(reverse(URL_BAD_REQUEST))

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