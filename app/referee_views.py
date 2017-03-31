from app.views import *

@login_required
def referee_evaluate_synopsis(request):
    """
    View method. Renders page for referee to evaluate PhD synopsis
    """
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))
    
    user = auth.get_user(request)
    referee = Referee.objects.get(user = user)
    
    if request.method == "GET":
        all_thesis = []     # list of dict
        
        for panelMember in PanelMember.objects.filter(referee = referee).filter(status = 'N'):
            thesis = panelMember.thesis
            dict = {}
            dict['title'] = thesis.title
            dict['student_full_name'] = thesis.student.first_name + " " + thesis.student.last_name
            dict['synopsis'] = thesis.synopsis
            dict['student_username'] = thesis.student.user.username
            dict['id'] = thesis.id
            
            all_thesis.append(dict)
        
        return render(request, 'app/referee/evaluate_synopsis.html', {
            'title':'Unevaluated PhD Synopsis',
            'layout_data' : get_layout_data(request),
            'all_thesis' : all_thesis
        })
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def referee_synopsis_approval(request):
    """
    Handles user request to approve/reject PhD synopsis
    """
    
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))
    
    user = auth.get_user(request)
    referee = Referee.objects.get(user = user)
    
    if request.method == "POST":
        id = int(request.POST['id'])
        isApproved = request.POST['isApproved'] == "True"
        feedback = request.POST['feedback']

        thesis = Thesis.objects.get(id = id)
        panelMember = PanelMember.objects.get(thesis = thesis, referee = referee)

        dict = {'status' : 'OK', 'message' : 'Your response has been submitted successfully' }
        
        #noentry = NoEntryPanel(thesis_id = thesis, referee_username = referee)
        #noentry.save()

        if isApproved:
            panelMember.status = 'A'
            panelMember.save()
        else:
            panelMember.status = 'R'
            panelMember.save()
            if referee.type == 'I':
                invite_indian_referee(thesis)
            else:
                invite_foreign_referee(thesis)
        
        
        ############################################################################
        # notify guides & co-guides ---notify only admin and director
        for thesisGuide in ThesisGuide.objects.filter(thesis = thesis):
            guide = thesisGuide.guide.user
            message = 'Referee ' + referee.user.first_name + ' ' + referee.user.last_name + ' '

            if isApproved:
                message += 'has approved to evaluate the PhD with title ' + thesis.title + '.'
            else:
                message += 'has rejected to evaluate the PhD with title ' + thesis.title + '.'

            if len(feedback.strip()) > 0:
                message += ' Referee has given the following feedback - ' + feedback

            send_notification(referee, guide, message, '')
        #################################################################################

        return HttpResponse(json.dumps(dict), content_type = 'application/json')
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def referee_evaluate_thesis(request):
    """
    View method. Renders page for referee to evaluate PhD thesis document
    """

    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    if request.method == "GET":
        return render(
            request,
            'app/referee/evaluate_thesis.html',
            {
                'title':'Evaluate Thesis',
                'layout_data' : get_layout_data(request),
            }
        )
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def referee_thesis_approval(request):
    """
    Handles user request to approve/reject thesis document
    """

    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))
    
    user = auth.get_user(request)
    referee = Referee.objects.get(user = user)
    
    if request.method == "POST":
        
        dict = {'status' : 'OK', 'message' : 'Your response has been submitted successfully' }

        return HttpResponse(json.dumps(dict), content_type = 'application/json')
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def referee_help_procedure(request):
    """
    View method. Renders page for procedure help
    """

    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    return render(
        request,
        'app/referee/procedure.html',
        {
            'title':'Procedure',
            'layout_data' : get_layout_data(request),
        }
    )

@login_required
def referee_help_contacts(request):
    """
    View method. Renders page for contact help
    """

    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    return render(
        request,
        'app/referee/help_contacts.html',
        {
            'title':'Help Contacts',
            'layout_data' : get_layout_data(request),
        }
    )