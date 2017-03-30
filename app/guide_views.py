from app.views import *
from django.db.models import Q

STATUS_ID_SUBMIT_ABSTRACT = 5
STATUS_ID_ABSTRACT_APPROVED = 7
STATUS_ID_SUBMIT_SYNOPSIS = 9
STATUS_ID_SYNOPSIS_APPROVED = 11
STATUS_ID_SUBMIT_THESIS = 13
STATUS_ID_THESIS_APPROVED = 15
STATUS_ID_PANEL_SENT = 19

def send_notification_to_other_guides(user, message, thesis):
    """
    Utility method which sends a message to the other guides
    and co-guides mentoring for the same PhD thesis

    Args:
        user: User model object
        message: string containing notification text
        thesis: Thesis model object
    """

    for thesisGuide in ThesisGuide.objects.filter(thesis = thesis):
        receiver = User.objects.get(username = thesisGuide.guide.user.username)

        if receiver != user:
            send_notification(user, receiver, message, '')

@login_required
def guide_unevaluated_abstract(request):
    """
    View method. Renders a page which lists out all the unevaluated PhD abstracts.
    """

    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))
    
    user = auth.get_user(request)
    guide = Faculty.objects.get(user = user)

    if request.method == "GET":
        all_thesis = []     # list of dict
        for thesisGuide in ThesisGuide.objects.filter(guide = guide):
            thesis = thesisGuide.thesis
            if thesis.status.id > STATUS_ID_SUBMIT_ABSTRACT and thesis.status.id < STATUS_ID_ABSTRACT_APPROVED:
                if not ThesisGuideApproval.objects.filter(thesis = thesis).filter(guide = guide).filter(type = 'A'):
                    dict = {}
                    dict['title'] = thesis.title
                    dict['student_full_name'] = thesis.student.first_name + ' ' + thesis.student.last_name
                    dict['abstract'] = thesis.abstract
                    dict['student_username'] = thesis.student.user.username
                    dict['id'] = thesis.id
                    all_thesis.append(dict)

        return render(
            request,
            'app/guide/unevaluated_abstract.html',
            {
                'title':'Unevaluated PhD Abstract',
                'layout_data' : get_layout_data(request),
                'all_thesis' : all_thesis
            }
        )
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def guide_evaluate_unevaluated_abstract(request):
    """
    Handles a user request to accept/reject a student's abstract.
    Returns a text/plain response
    """
    
    if request.method == "POST":
        user = auth.get_user(request)
        guide = Faculty.objects.get(user = user)
        thesisid = int(request.POST['id'])
        isApproved = request.POST['isApproved'] == "True"
        feedback = request.POST['feedback']
        thesis = Thesis.objects.get(id = thesisid)
        
        if isApproved:
            thesisGuideApprovals = ThesisGuideApproval(thesis = thesis, guide = guide, type = 'A')
            thesisGuideApprovals.save()
            # notify student about approval
            notification_message = request.session['full_name'] + " had accepted the abstract submitted "
            send_notification(user, thesis.student.user, notification_message, '')
        else:
            # need to downgrade status after reject, and remove abstract
            # delete others approvals
            thesisGuideApprovals = ThesisGuideApproval.objects.filter(thesis = thesis).filter(type = 'A')
            thesisGuideApprovals.delete()
            # notify other guides about rejection
            notification_message = request.session['full_name'] + " had rejected the abstract submitted by '" + thesis.student.first_name
            send_notification_to_other_guides(user, notification_message, thesis)
            # notify student about rejection
            notification_message = request.session['full_name'] + " had rejected the abstract submitted "
            notification_message += "\nFeedback: " + feedback
            send_notification(user, thesis.student.user, notification_message, '')

        return HttpResponse('0', content_type = 'text/plain')
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def guide_unevaulated_synopsis(request):
    """
    View method. Renders a page which allows guide to
    view PhD synopsis submitted by students
    """

    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))
    
    user = auth.get_user(request)
    guide = Faculty.objects.get(user = user)

    if request.method == "GET":
        all_thesis = []     # list of dict
        
        for thesisGuides in ThesisGuide.objects.filter(guide = guide):
            thesis = thesisGuides.thesis
            if thesis.status.id > STATUS_ID_SUBMIT_SYNOPSIS and thesis.status.id < STATUS_ID_SYNOPSIS_APPROVED:
                if not ThesisGuideApproval.objects.filter(thesis = thesis).filter(guide = guide).filter(type = 'S'):
                    dict = {}
                    dict['title'] = thesis.title
                    dict['student_full_name'] = thesis.student.first_name + ' ' + thesis.student.last_name
                    dict['abstract'] = thesis.abstract
                    dict['synopsis'] = thesis.synopsis
                    dict['student_username'] = thesis.student.user.username
                    dict['id'] = thesis.id
                    all_thesis.append(dict)
        return render(
            request,
            'app/guide/unevaluated_synopsis.html',
            {
                'title':'Unevaluated PhD Synopsis',
                'layout_data' : get_layout_data(request),
                'all_thesis' : all_thesis
            }
        )
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def guide_evaluate_unevaluated_synopsis(request):
    """
    Handles user request to approve/reject a submitted PhD synopsis
    """

    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    if request.method == "POST":
        user = auth.get_user(request)
        guide = Faculty.objects.get(user = user)
        thesisid = int(request.POST['id'])
        isApproved = request.POST['isApproved'] == "True"
        feedback = request.POST['feedback']
        thesis = Thesis.objects.get(id = thesisid)
        
        if isApproved:
            thesisGuideApprovals = ThesisGuideApproval(thesis = thesis, guide = guide, type = 'S')
            thesisGuideApprovals.save()
            # notify student about approval
            notification_message = request.session['full_name'] + " had accepted the synopsis submitted "
            send_notification(user, thesis.student.user, notification_message, '')
        else:
            # need to downgrade status after reject, and remove abstract
            # delete others approvals
            thesisGuideApprovals = ThesisGuideApproval.objects.filter(thesis = thesis).filter(type = 'S')
            thesisGuideApprovals.delete()
            # notify other guides about rejection
            notification_message = request.session['full_name'] + " had rejected the synopsis submitted by '" + thesis.student.first_name
            send_notification_to_other_guides(user, notification_message, thesis)
            # notify student about rejection
            notification_message = request.session['full_name'] + " had rejected the synopsis submitted "
            notification_message += "\nFeedback: " + feedback
            send_notification(user, thesis.student.user, notification_message, '')
        return HttpResponse('0', content_type = 'text/plain')
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def guide_unevaluated_thesis(request):
    """
    View method. Renders a page for guide to view unevaluated thesis documents
    """

    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))
    
    user = auth.get_user(request)
    guide = Faculty.objects.get(user = user)

    if request.method == "GET":
        all_thesis = []     # list of dict
        for thesisGuides in ThesisGuide.objects.filter(guide = guide):
            thesis = thesisGuides.thesis
            if thesis.status.id > STATUS_ID_SUBMIT_THESIS and thesis.status.id < STATUS_ID_THESIS_APPROVED:
                if not ThesisGuideApproval.objects.filter(thesis = thesis).filter(guide = guide).filter(type = 'T'):
                    dict = {}
                    dict['title'] = thesis.title
                    dict['student_full_name'] = thesis.student.first_name + " " + thesis.student.last_name
                    dict['abstract'] = thesis.abstract
                    dict['thesis'] = thesis.thesis
                    dict['student_username'] = thesis.student.user.username
                    dict['id'] = thesis.id
                    all_thesis.append(dict)
        return render(
            request,
            'app/guide/unevaluated_thesis.html',
            {
                'title':'Unevaluated PhD Thesis',
                'layout_data' : get_layout_data(request),
                'all_thesis' : all_thesis
            }
        )
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def guide_evaluate_unevaluated_thesis(request):
    """
    Handles a user request to approve/reject a PhD thesis
    """

    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    if request.method == "POST":
        user = auth.get_user(request)
        guide = Faculty.objects.get(user = user)
        thesisid = int(request.POST['id'])
        isApproved = request.POST['isApproved'] == "True"
        feedback = request.POST['feedback']
        thesis = Thesis.objects.get(id = thesisid)
        
        if isApproved:
            thesisGuideApprovals = ThesisGuideApproval(thesis = thesis, guide = guide, type = 'T')
            thesisGuideApprovals.save()
            #notify student about approval
            notification_message = request.session['full_name'] + " had accepted the thesis submitted "
            send_notification(user, thesis.student.user, notification_message, '')
        else:
            # need to downgrade status after reject, and remove abstract
            # delete others approvals
            thesisGuideApprovals = ThesisGuideApproval.objects.filter(thesis = thesis).filter(type = 'T')
            thesisGuideApprovals.delete()
            # notify other guides about rejection
            notification_message = request.session['full_name'] + " had rejected the thesis submitted by '" + thesis.student.first_name
            send_notification_to_other_guides(user, notification_message, thesis)
            # notify student about rejection
            notification_message = request.session['full_name'] + " had rejected the thesis submitted "
            notification_message += "\nFeedback: " + feedback
            send_notification(user, thesis.student.user, notification_message, '')
        return HttpResponse('0', content_type = 'text/plain')
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def guide_phd_status(request):
    """
    View method. Renders a page which displays the status of all the PhDs under the guide
    """

    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    if request.method == "GET":
        user = auth.get_user(request)
        guide = Faculty.objects.get(user = user)
        all_thesis = []     # list of dict
        for thesisGuides in ThesisGuide.objects.filter(guide = guide):
            thesis = thesisGuides.thesis
           
            dict = {}
            dict['title'] = thesis.title
            dict['student_full_name'] = thesis.student.first_name + " " + thesis.student.last_name
            dict['student_username'] = thesis.student.user.username
            dict['id'] = thesis.id
            dict['status_message'] = thesis.status.status_message
            all_thesis.append(dict)
        return render(
            request,
            'app/guide/phd_status.html',
            {
                'title':'PhD Status',
                'layout_data' : get_layout_data(request),
                'all_thesis' : all_thesis
            }
        )
    else:
        return redirect(reverse(URL_BAD_REQUEST))

def _get_referee_details(str, type):
    """
    Gets all the referees of the given 'type' with their name matching with 'str'
    """

    users = User.objects.filter(Q(first_name__icontains = str) | Q(last_name__icontains = str))
    print("users successful")
    referees = Referee.objects.filter(type = type).filter(user__in = users)
    
    print("in succesful")
    result = []
    for referee in referees:
        print("inside for")
        dict = {}
        dict['text'] = referee.user.first_name + ' ' + referee.user.last_name
        dict['email'] = referee.user.email
        dict['id'] = referee.id
        dict['username'] = referee.user.username
        result.append(dict)

    return result

@login_required
def guide_get_foreign_referee_details(request):
    """
    Handles a user request for foreign referee details
    Outputs JSON
    """

    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    if request.method == "GET":
        name = request.GET['term']

        return HttpResponse(json.dumps(_get_referee_details(name, 'F')), content_type = 'application/json')
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def guide_get_indian_referee_details(request):
    """
    Handles a user request for indian referee details
    Outputs JSON
    """

    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    if request.method == "GET":
        name = request.GET['term']

        return HttpResponse(json.dumps(_get_referee_details(name, 'I')), content_type = 'application/json')
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def guide_submit_evaluation_panel(request):
    """
    View method. Renders a page which allows guide to submit a referee panel
    """

    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    if request.method == "GET":
        user = auth.get_user(request)
        guide = Faculty.objects.get(user = user)
        all_thesis = []     # list of dict

       
        #all_thesis shud have 4 list of dict objects
        #for thesis in all_thesis:
        #    thesis.other_selected_indian_referees = [dict, dict, dict]
        #    dict['username'] -> referee username
        #    dict['full_name'] -> referee full_name
        #    dict['added_by_guide_username'] -> username of guide who added it
        #    dict['added_by_guide_full_name'] -> full_name of guide who added it
        #    dict['added_by_guide_type'] -> type of guide who added it (guide/co-guide)

        #    a similar dictionary for foreign referees with same dictionary keys and values
        #    thesis.other_selected_indian_referees = [dict, dict, dict,]


        #    a dictionary consisting of foriegn referees selected by logged in guide
        #    thesis.foreign_referees = [dict, dict, dict, ]
        #    dict['username'] = referee id, id of this referee's entry in User table
        #    dict['full_name'] = referee full name

        #    a similar dictionary for indian referees with same dictionary keys and values
        #    thesis.indian_referees = [dict, dict, dict, ]

        #   thesis.guide_type = 'C' or 'G' denoting whether currently logged in faculty is a guide/co-guide to this thesis

        for thesisGuides in ThesisGuide.objects.filter(guide = guide):
            thesis = thesisGuides.thesis
            # check the status i.e., Here the submitted thesis must be approved b all guide/co-guide
            if thesis.status.id >= STATUS_ID_THESIS_APPROVED and thesis.status.id < STATUS_ID_PANEL_SENT:
                # this 'if can be avoided,if status is used properly 
                if not PanelMember.objects.filter(thesis = thesis):
                    dict = {}
                    dict['title'] = thesis.title
                    dict['student_full_name'] = thesis.student.first_name + " " + thesis.student.last_name
                    dict['student_username'] = thesis.student.user.username
                    dict['id'] = thesis.id
                    all_thesis.append(dict)
        return render(
            request,
            'app/guide/submit_evaluation_panel.html',
            {
                'title':'Procedure',
                'layout_data' : get_layout_data(request),
                'all_thesis' : all_thesis
            }
        )
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def guide_send_panel_to_director(request):
    """
    Handles a request from a guide to send panel members to the director
    """
    if request.method == "POST":
        # do stuff

        dict = {'status' : 'OK', 'message' : 'Panel successfully sent to director!'}

        return HttpResponse(json.dumps(dict), content_type = 'application/json')
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def guide_save_panel_members(request):
    """
    Handles a user request to add referee panel members for a thesis
    """
    
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    if request.method == "POST":
        # list of integer strings which are ids in the User table
        # corresponding to the indian/foreign referee
        indian_referees = request.POST.getlist('indian_referees[]')
        foreign_referees = request.POST.getlist('foreign_referees[]')
        id = int(request.POST['id'])   # thesis id

        # add referees for corresponding thesis and send notifications accordingly
        thesis = Thesis.objects.get(id = id)
        
        #adding indian
        for indian in indian_referees:
            referee = Referee.objects.get(id = int(indian))
            panel_member = PanelMember(thesis = thesis, referee = referee, priority = 0, status = 'U')
            panel_member.save()
        #adding foreign
        for foreign in foreign_referees:
            referee = Referee.objects.get(id = int(foreign))
            panel_member = PanelMember(thesis = thesis, referee = referee, priority = 0, status = 'U')
            panel_member.save()


        user = auth.get_user(request)
        director = Approver.objects.filter(active = true)[0].faculty.user
        #send notification to student
        send_notification(user, thesis.student.user, "Congratulations! Your thesis had been sent for Evaluation.Stay tuned for results", '')
        #send notification to director
        send_notification(user, director, "Panel had been sent for evaluation of " + thesis.student.first_name + " ", '')
        #upgrade status

        dict = {'status' : 'OK', 'message' : 'Panel Members added successfully!'}

        return HttpResponse(json.dumps(dict), content_type = 'text/json')
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def guide_help_procedure(request):
    """
    View method. Renders procedure help page.
    """

    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    return render(
        request,
        'app/guide/procedure.html',
        {
            'title':'Procedure',
            'layout_data' : get_layout_data(request),
        }
    )

@login_required
def guide_help_contacts(request):
    """
    View method. Renders contacts help page.
    """

    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    return render(
        request,
        'app/guide/help_contacts.html',
        {
            'title':'Help Contacts',
            'layout_data' : get_layout_data(request),
        }
    )