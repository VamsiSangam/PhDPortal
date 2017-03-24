from app.views import *
STATUS_ID_SUBMIT_ABSTRACT = 5
STATUS_ID_ABSTRACT_APPROVED = 7
STATUS_ID_SUBMIT_SYNOPSIS = 9
STATUS_ID_SYNOPSIS_APPROVED = 11
STATUS_ID_SUBMIT_THESIS = 13
STATUS_ID_THESIS_APPROVED = 15

def send_notification_to_other_guides(username, message, thesis):
    user = User.objects.get(username = username)
    for guide in ThesisGuides.objects.filter(thesis_id = thesis):
        receiver = User.objects.get(username = guide.guide_username.username)
        if receiver != username:
            send_notification(user, receiver, message, '')

@login_required
def guide_unevaluated_abstract(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))
    
    user = User.objects.get(username = request.session['username'])

    if request.method == "GET":
        all_thesis = []     # list of dict
        for thesisGuides_object in ThesisGuides.objects.filter(guide_username = user):
            thesis_object = thesisGuides_object.thesis_id
            if thesis_object.status.id > STATUS_ID_SUBMIT_ABSTRACT and thesis_object.status.id < STATUS_ID_ABSTRACT_APPROVED:
                if not ThesisGuideApprovals.objects.filter(thesis = thesis_object).filter(guide = user).filter(type = 'A'):
                    dict = {}
                    dict['title'] = thesis_object.title
                    dict['student_full_name'] = thesis_object.username.first_name+" "+thesis_object.username.last_name
                    dict['abstract'] = thesis_object.abstract
                    dict['student_username'] = thesis_object.username
                    dict['id'] = thesis_object.id
                    all_thesis.append(dict)

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
        user = User.objects.get(username = request.session['username'])
        thesisid = int(request.POST['id'])
        isApproved = request.POST['isApproved'] == "True"
        feedback = request.POST['feedback']
        thesis = Thesis.objects.get(id = thesisid)
        
        if isApproved:
            thesisGuideApprovals = ThesisGuideApprovals(thesis = thesis, guide = user, type = 'A')
            thesisGuideApprovals.save()
            #notify student about approval
            notification_message = request.session['username'] + " had accepted the abstract submitted "
            send_notification(user, thesis.username, notification_message, '')
        else:
            # need to downgrade status after reject, and remove abstract
            # delete others approvals
            thesisGuideApprovals = ThesisGuideApprovals.objects.filter(thesis = thesis).filter(type = 'A')
            thesisGuideApprovals.delete()
            #notify other guides about rejection
            notification_message = request.session['username'] + " had rejected the abstract submitted by '" + thesis.username.username
            send_notification_to_other_guides(request.session['username'], notification_message, thesis)
            #notify student about rejection
            notification_message = request.session['username'] + " had rejected the abstract submitted "
            notification_message += "\nFeedback: " + feedback
            send_notification(user, thesis.username, notification_message, '')

        return HttpResponse('0', content_type = 'text/plain')
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def guide_unevaulated_synopsis(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))
    
    user = User.objects.get(username = request.session['username'])

    if request.method == "GET":
        # query for all the thesis under this guide 
        # whose synopsis was not evaluated by this guide
        
        all_thesis = []     # list of dict

        # each element of all_thesis is a dict
        # dict['title'] = phd title
        # dict['student_full_name'] = student full name
        # dict['abstract'] = phd abstract
        # dict['synopsis'] = phd synopsis
        # dict['student_username'] = student_username
        # dict['id'] = thesis_id (int)

        return render(
            request,
            'app/guide/unevaluated_synopsis.html',
            {
                'title':'Unevaluated PhD Synopsis',
                'descriptive_title' : 'View unevaluated synopsis sumitted by PhD students',
                'unread_notifications' : get_unread_notifications(request.session['username']),
                'all_thesis' : all_thesis
            }
        )
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def guide_evaluate_unevaluated_synopsis(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    if request.method == "POST":
        # read post data
        # request.POST['id'] = string - thesis id
        # request.POST['isApproved'] = 'true' / 'false'
        # request.POST['feedback'] = feedback string
        # if true add row into ThesisGuideApprovals, with type = 'S'
        # if false remove all approvals for this thesis synopsis so far
        # send notifications accordingly

        return HttpResponse('0', content_type = 'text/plain')
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def guide_unevaluated_thesis(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))
    
    user = User.objects.get(username = request.session['username'])

    if request.method == "GET":
        # query for all the thesis under this guide 
        # whose thesis document was not evaluated by this guide
        
        all_thesis = []     # list of dict

        # each element of all_thesis is a dict
        # dict['title'] = phd title
        # dict['student_full_name'] = student full name
        # dict['abstract'] = phd abstract
        # dict['thesis'] = phd thesis
        # dict['student_username'] = student_username
        # dict['id'] = thesis_id (int)

        return render(
            request,
            'app/guide/unevaluated_thesis.html',
            {
                'title':'Unevaluated PhD Thesis',
                'descriptive_title' : 'View unevaluated thesis sumitted by PhD students',
                'unread_notifications' : get_unread_notifications(request.session['username']),
                'all_thesis' : all_thesis
            }
        )
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def guide_evaluate_unevaluated_thesis(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    if request.method == "POST":
        # read post data
        # request.POST['id'] = string - thesis id
        # request.POST['isApproved'] = 'true' / 'false'
        # request.POST['feedback'] = feedback string
        # if true add row into ThesisGuideApprovals, with type = 'T'
        # if false remove all approvals for this thesis synopsis so far
        # send notifications accordingly

        return HttpResponse('0', content_type = 'text/plain')
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def guide_phd_status(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    if request.method == "GET":
        # query for all the thesis under this guide 
        
        all_thesis = []     # list of dict

        # each element of all_thesis is a dict
        # dict['title'] = phd title
        # dict['student_full_name'] = student full name
        # dict['student_username'] = student_username
        # dict['id'] = thesis_id (int)
        # dict['status_message'] = status message correspsonding to phd status id

        return render(
            request,
            'app/guide/phd_status.html',
            {
                'title':'PhD Status',
                'descriptive_title' : 'View the status of ongoing PhDs',
                'unread_notifications' : get_unread_notifications(request.session['username']),
                'all_thesis' : all_thesis
            }
        )
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def guide_submit_evaluation_panel(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    if request.method == "GET":

        return render(
            request,
            'app/guide/submit_evaluation_panel.html',
            {
                'title':'Procedure',
                'descriptive_title' : 'Submit PhD Evaluation Panel',
                'unread_notifications' : get_unread_notifications(request.session['username'])
            }
        )
    else:
        return redirect(reverse(URL_BAD_REQUEST))


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