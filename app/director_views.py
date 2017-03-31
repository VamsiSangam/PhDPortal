from app.views import *
from app.student_views import *

@login_required
def director_view_student_info(request):
    """
    View method. Renders student info page
    """

    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    if request.method == "GET":
        all_thesis = []     # list of dict
        for thesis in Thesis.objects.all():
            dict = {}
            dict['title'] = thesis.title
            dict['student_full_name'] = thesis.student.first_name + " " + thesis.student.last_name
            dict['student_username'] = thesis.student.user.username
            dict['id'] = thesis.id
            dict['status_message'] = thesis.status.status_message
            all_thesis.append(dict)
        return render(
            request,
            'app/director/view_student_info.html',
            {
                'title':'PhD Status',
                'layout_data' : get_layout_data(request),
                'all_thesis' : all_thesis
            }
        )
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def director_submit_for_evaluation(request):
    """
    View method. Renders page for director to choose panel
    """
    
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))
    
    if request.method == "GET": 
        all_list = []     # list of dict
        for thesis in Thesis.objects.all():
            this_thesis = {}
        
            #need to use one more status if referees are out of bound
            if thesis.status.id >= STATUS_ID_PANEL_APPROVED and thesis.status.id < STATUS_ID_THESIS_UNDER_EVALUATION:
            #if  PanelMember.objects.filter(thesis = thesis,status='G'):  
                #storing thesis information
                this_thesis['id'] = thesis.id
                this_thesis['username'] = thesis.student.user.username
                this_thesis['fullname'] = thesis.student.user.first_name + " " + thesis.student.user.last_name
                this_thesis['title'] = thesis.title
                this_thesis['abstract'] = thesis.abstract
                this_thesis['guides'] = []
                #storing guides of a thesis
                for thesis_guides in ThesisGuide.objects.filter(thesis = thesis):
                    dict = {}
                    dict['username'] = thesis_guides.guide.user.username
                    dict['fullname'] = thesis_guides.guide.user.first_name + " " + thesis_guides.guide.user.last_name
                    if thesis_guides.type == 'G':
                        dict['type'] = 'Guide'
                    else:
                        dict['type'] = 'Co-Guide'
                    this_thesis['guides'].append(dict)
                #storing referee information
                this_thesis['indian_referees'] = []
                this_thesis['foreign_referees'] = []
                for panel in PanelMember.objects.filter(thesis = thesis,status = 'G'): #if the panel is approved by guides only only
                    dict = {}
                    logger.info("********" + str(thesis.id) +" "+(panel.referee.user).username+ "*********")
                    dict['username'] = panel.referee.user.username
                    dict['fullname'] = panel.referee.user.first_name + " " + panel.referee.user.last_name
                    dict['address'] = "No yet included in database"  #Need to change
                    dict['designation'] = panel.referee.designation
                    dict['website'] = panel.referee.website
                    dict['university'] = panel.referee.university
                    referee = panel.referee
                    if referee.type == 'I':
                        dict['type'] = 'Indian'
                        this_thesis['indian_referees'].append(dict)
                    else:
                        dict['type'] = 'Foreign'
                        this_thesis['foreign_referees'].append(dict)
                #storing thesis keywords
                this_thesis['keywords'] = []
                for keys in ThesisKeyword.objects.filter(thesis = thesis):
                    this_thesis['keywords'].append((IEEEKeyword.objects.get(id = keys.keyword.id)).keyword)
                
                this_thesis['required_indian'] = thesis.indian_referees_required
                this_thesis['required_foreign'] = thesis.foreign_referees_required
                
                for finalpanel in PanelMember.objects.filter(thesis = thesis):
                    referee = finalpanel.referee
                    if referee.type == 'I' and finalpanel.status == 'A':
                        this_thesis['required_indian'] -= 1
                    if referee.type == 'F' and finalpanel.status == 'A':
                        this_thesis['required_foreign'] -= 1
                all_list.append(this_thesis)
             
        return render(
            request,
            'app/director/submit_for_evaluation.html',
            {
                'title':'List of Students',
                'descriptive_title' : 'View and shortlist Panel Sent by Guide For Final evaluation',
                'unread_notifications' : get_unread_notifications(request.session['username']),
                'all_list' : all_list
            }
        )
    elif request.method == "POST":
        #Post request in director page
        total_indian = int(request.POST['total_indian'])
        total_foreign = int(request.POST['total_foreign'])
        required_indian = int(request.POST['required_indian'])
        required_foreign = int(request.POST['required_foreign'])
        thesis_id = int(request.POST['thesis_id'])
        indian = []
        foreign = []
        count_indian = 0
        count_foreign = 0
        # server-side checking if the input filled is in/correct format
        hashmap = {}
        for i in range(1,total_indian+1):
            name_case = 'indian-referee-' + str(i)
            username = request.POST[name_case]
            if username != 'none':
                if not hashmap.get(username):
                    indian.append(username)
                    count_indian += 1
                    hashmap[username] = 'True'
                else:  #When user selects same referee multiple times
                    return redirect(reverse(URL_BAD_REQUEST))
         
        hashmap.clear()
        for i in range(1,total_foreign+1):
            name_case = 'foreign-referee-' + str(i)
            username = request.POST[name_case]
            if username != 'none':
                if not hashmap.get(username):
                    foreign.append(username)
                    count_foreign += 1
                    hashmap[username] = 'True'
                else: #When user selects same referee multiple times
                    return redirect(reverse(URL_BAD_REQUEST))
 
        
        #When number of referees choosen didn't reach the minimum limit
        if count_indian < required_indian or count_foreign < required_foreign:
            return redirect(redirect(reverse(URL_BAD_REQUEST)))

        #start actual process of automation

        #delete thesis panel info from panelmembers (guide submitted one)
        thesis = Thesis.objects.get(id = thesis_id)

        #storing the priotiy list in FinalPanel
        for i in range(0,count_indian):
            user = User.objects.get(username=indian[i])
            finalpanel = PanelMember.objects.get(thesis = thesis, referee = user)
            finalpanel.priority = i+1
            finalpanel.status = 'N'
            finalpanel.save()
        for i in range(0,count_foreign):
            user = User.objects.get(username=foreign[i])
            finalpanel = PanelMember.objects.get(thesis = thesis, referee = user)
            finalpanel.priority = i+1
            finalpanel.status = 'N'
            finalpanel.save()

        #sending the referees notifications and emails (only the top priotity one)
        invite_indian_referees(thesis)
        invite_foreign_referees(thesis)
        return redirect(reverse(director_submit_for_evaluation))

def invite_indian_referees(thesis):
    finalpanel = PanelMember.objects.filter(thesis = thesis).filter(Q(status = 'A') | Q(status = 'S')) #do not consider invite_sent and approved
    
    totalApprovals = 0 #both approved and already requested i.e.,to get total number of invitations to be done
    for panel in finalpanel:
        if Referee.objects.get(referee = panel.referee).type == 'I':
            totalApprovals += 1

    totalRequired = thesis.indian_referees_required - totalApprovals #Total number of invitations to send
    
    director = (Approver.objects.filter(active = True)[0]).faculty.user

    for referee in PanelMember.objects.filter(thesis = thesis).filter(status = 'N').order_by('priority'):
        if referee.referee.type == 'I':
            if totalRequired == 0:
                break
            #send notification to that referee
            message = "You have received an invitation to evaluate a thesis with title \"" + thesis.title + "\""
            send_notitfication(director, referee.referee.user, message, '')
            #send email --fill this afterwards
            totalRequired -= 1
            referee.status = 'S' #until his decision
            referee.save()

    if totalRequired != 0:
        #request a new panel from guide
        #Note: Update the status also --Flow maintainance
        message = "Dear sir, you need to re-submit a panel list for the student " + thesis.student.user.username
        send_notification_to_other_guides(director, message, thesis)
        #email also
        request = RequestPanel(thesis = thesis)
        request.save()

def invite_foreign_referees(thesis):
    finalpanel = PanelMember.objects.filter(thesis = thesis).filter(Q(status = 'A') | Q(status = 'S')) #do not consider invite_sent and approved
    
    totalApprovals = 0 #both approved and already requested i.e.,to get total number of invitations to be done
    for panel in finalpanel:
        if Referee.objects.get(referee = panel.referee).type == 'F':
            totalApprovals += 1

    totalRequired = thesis.indian_referees_required - totalApprovals #Total number of invitations to send
    
    director = (Approver.objects.filter(active = True)[0]).faculty.user

    for referee in PanelMember.objects.filter(thesis = thesis).filter(status = 'N').order_by('priority'):
        if referee.referee.type == 'F':
            if totalRequired == 0:
                break
            #send notification to that referee
            message = "You have received an invitation to evaluate a thesis with title \"" + thesis.title + "\""
            send_notitfication(director, referee.referee.user, message, '')
            #send email --fill this afterwards
            totalRequired -= 1
            referee.status = 'S' #until his decision
            referee.save()

    if totalRequired != 0:
        #request a new panel from guide
        #Note: Update the status also --Flow maintainance
        message = "Dear sir, you need to re-submit a panel list for the student " + thesis.student.user.username
        send_notification_to_other_guides(director, message, thesis)
        #email also
        request = RequestPanel(thesis = thesis)
        request.save()

@login_required
def director_help_procedure(request):
    """
    View method. Renders procedure help page.
    """

    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    return render(
        request,
        'app/director/procedure.html',
        {
            'title':'Procedure',
            'layout_data' : get_layout_data(request),
        }
    )

@login_required
def director_help_contacts(request):
    """
    View method. Renders contact help page.
    """

    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    return render(
        request,
        'app/director/help_contacts.html',
        {
            'title':'Help Contacts',
            'layout_data' : get_layout_data(request),
        }
    )