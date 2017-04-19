from app.views import *
from app.student_views import _update_student_status
from django.db.models import Q

from app.tasks import send_email_task

STATUS_ID_SUBMIT_ABSTRACT = 5
STATUS_ID_ABSTRACT_WAITING_APPROVAL = 6
STATUS_ID_ABSTRACT_APPROVED = 8
STATUS_ID_SUBMIT_SYNOPSIS = 9
STATUS_ID_SYNOPSIS_WAITING_APPROVAL = 10
STATUS_ID_SYNOPSIS_APPROVED = 12
STATUS_ID_SUBMIT_THESIS = 13
STATUS_ID_THESIS_WAITING_APPROVAL = 14
STATUS_ID_THESIS_APPROVED = 16
STATUS_ID_WAITING_FOR_PANEL_APPROVAL = 17
STATUS_ID_PANEL_SENT = 18
STATUS_ID_PANEL_SUBMITTED_BY_DIRECTOR = 20
STATUS_ID_THESIS_UNDER_EVALUATION = 21
STATUS_ID_THESIS_FEEDBACKS_RECEIVED = 22
STATUS_ID_ASKED_FOR_MODIFICATIONS = 23
STATUS_ID_CALL_FOR_VIVAVOICE = 24

def send_notification_to_all_guides(sender, thesis, message):
    """
    Sends a notification with given 'message' to
    all the guides mentoring given 'student'
    TODO: Notification model has link column which is still left un-utilized

    Args:
        user: User model object (of corresponding student)
        message: string object
    """

    for thesisGuide in ThesisGuide.objects.filter(thesis = thesis):
        receiver = User.objects.get(username = thesisGuide.guide.user.username)
        send_notification(sender, receiver, message, '')


@login_required
def admin_add_referee(request):
    
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))
    user = auth.get_user(request)
    
    dict = {'status' : 'Not-Done', 'message' : 'Something went Wrong,Try again later!' }
    if request.method == 'POST': 
        user_form = UserForm(request.POST)
        referee_form = RefereeForm(request.POST)

        if user_form.is_valid() and referee_form.is_valid():
            
            new_user = user_form.save(commit = False)
            new_user.is_active = True
            passwd = 'HelloWorld'
            new_user.set_password(passwd)
            new_user.save()
            #to get added_by key
            new_referee = referee_form.save(commit = False)
            new_referee.added_by = user
            new_referee.user = new_user
            new_referee.save()

            #send notification to that referee
            notify = "Hi sir/Madam! Welcome to the PhDPortal if IIIT-Allahabad.Please Update your Password"
            message = "You are added to the PhDPortal of IIIT-Allahabad.Please kindly check the Portal and update your Password.<br>Username is "+ str(request.POST.get('username')) + "<br>Password is" + passwd + "<br>"
            send_notification(user, new_user, notify, '')
            #send email --fill this afterwards
            #email to referee
            subject = "[Invitation]"
            content = "<br>Dear sir,</br><br></br><br></br>"+message+'. Please Check the PhD Portal for more details.'+"<br></br><br></br>Regards,<br></br>PhDPortal."

            email = []
            receiver = new_user
            email.append(receiver.email)
            send_email_task.delay(email, subject, content)

            dict = {'status' : 'Done', 'message' : 'Added the referee Successfully!' }
            
            
    elif request.method == 'GET':
        user_form = UserForm()
        referee_form = RefereeForm()

    else:
        #simply
        return redirect(reverse(URL_BAD_REQUEST))
    
    return render(request, 'app/admin/add_referee.html', 
        {'userform': user_form,
         'refereeform': referee_form,
         'dict' :dict,
        'layout_data': get_layout_data(request)
        })
    
@login_required
def admin_approve_referee(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))
    user = auth.get_user(request)
    suggested_referees = []
    dict = {}
    for referee in User.objects.filter(is_active = False):
            ref = Referee.objects.get(user = referee)
            dict = {}
            dict['referee'] = referee.username
            dict['full_name'] = referee.first_name + ' ' + referee.last_name
            guide_user = User.objects.get(id = ref.added_by.id)
            guide = Faculty.objects.get(user = guide_user)
            dict['added_by'] = guide.first_name + ' ' + guide.middle_name +' ' + guide.last_name
            user_form = UserForm(instance = referee)
            referee_form = RefereeForm(instance = ref)
            dict['userform'] = user_form
            dict['refereeform'] = referee_form
            suggested_referees.append(dict)
    
    if request.method == 'POST': 
        existing_user = User.objects.get(username = request.POST['referee_username'])
        existing_referee = Referee.objects.get(user = existing_user)

        user_form = UserForm(request.POST, instance = existing_user)
        referee_form = RefereeForm(request.POST, instance = existing_referee)    
        if user_form.is_valid() and referee_form.is_valid():
            passwd = 'HelloWorld' ##change this to customized timestamp
            existing_user.set_password(passwd)
            existing_user.is_active = True
            existing_user.save()
            user_form.save()
            referee_form.save()
            
            #send notification to that referee
            notify = "Hi sir/Madam! Welcome to the PhDPortal of IIIT-Allahabad.Please Update your Password."
            message = "You are added to the PhDPortal of IIIT-Allahabad.Please kindly check the Portal and update your Password.<br>Username is "+ str(request.POST.get('username')) + "<br>Password is" + passwd + "<br>"
            send_notification(user, existing_user, notify, '')
            #send email --fill this afterwards
            #email to referee
            subject = "[Invitation]"
            content = "<br>Dear sir,</br><br></br><br></br>"+message+'. Please Check the PhD Portal for more details.'+"<br></br><br></br>Regards,<br></br>PhDPortal."

            email = []
            receiver = existing_user
            email.append(receiver.email)
            send_email_task.delay(email, subject, content)
            
            dict = {'status' : 'Done', 'message' : 'Added the referee Successfully!' }
        else:
            dict = {'status' : 'Not-Done', 'message' : 'Something went Wrong,Try again later!Fill fields appropriately' }
            
    #elif request.method == 'GET':
    #    for referee in User.objects.filter(is_active = False):
    #        ref = Referee.objects.get(user = referee)
    #        dict = {}
    #        dict['referee'] = referee.username
    #        dict['full_name'] = referee.first_name + ' ' + referee.last_name
    #        guide_user = User.objects.get(id = ref.added_by.id)
    #        guide = Faculty.objects.get(user = guide_user)
    #        dict['added_by'] = guide.first_name + ' ' + guide.middle_name +' ' + guide.last_name
    #        user_form = UserForm(instance = referee)
    #        referee_form = RefereeForm(instance = ref)
    #        dict['userform'] = user_form
    #        dict['refereeform'] = referee_form
    #        suggested_referees.append(dict)
    #else:
    #    #simply
    #    return redirect(reverse(URL_BAD_REQUEST))
    
    return render(request, 'app/admin/approve_referee.html', 
        {'dict' :dict,
         'suggested_referees' : suggested_referees,
        'layout_data': get_layout_data(request)
        })

@login_required
def admin_evaluate_reports(request):
    """
    Admin need to verify the feedback sent by referees
    and forward it to respective guides
    """
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))
    
    admin = auth.get_user(request)
    
    if request.method == "GET":
        all_thesis = []     # list of dict
        
        for panelmember in PanelMember.objects.filter(Q(status = 'F') | Q(status = 'Z')).filter(feedback_at = 'A'):
            thesis = panelmember.thesis
            dict = {}
            dict['title'] = thesis.title
            dict['student_full_name'] = thesis.student.first_name + " " + thesis.student.last_name
            dict['report'] = panelmember.feedback_with_referee_details
            dict['student_username'] = thesis.student.user.username
            dict['id'] = thesis.id
            dict['referee_name'] = panelmember.referee.user.first_name + ' ' + panelmember.referee.user.last_name
            dict['referee_id'] = panelmember.referee.id
            print(panelmember.referee.id)

            all_thesis.append(dict)
        
        return render(request, 'app/admin/view_finalReports.html', {
            'title':'Final Reports',
            'layout_data' : get_layout_data(request),
            'all_thesis' : all_thesis
        })
    elif request.method == "POST":
        thesis = int(request.POST['thesis'])
        referee = int(request.POST['referee'])
        referee = Referee.objects.get(id = referee)
        thesis = Thesis.objects.get(id = thesis)
        panelmember = PanelMember.objects.get(thesis = thesis,referee = referee)
        panelmember.feedback_at = 'G'
        
        panelmember.save()

        total_feedbacks = PanelMember.objects.filter(thesis = thesis, feedback_at = 'G').count()
        if total_feedbacks == thesis.indian_referees_required + thesis.foreign_referees_required:
            _update_student_status(thesis, STATUS_ID_THESIS_FEEDBACKS_RECEIVED) 

        dict = {'status' : 'OK', 'message' : 'Feedback Report Sent Successfully!'}
        #send notification to all guide
        send_notification_to_all_guides(admin, thesis, "A feedback report has been sent of student " + thesis.student.first_name + " " + thesis.student.last_name)
        #email
        subject = "[Feed Back reports] of the Thesis titled" + thesis.title
        content = "<br>Dear Sir/Madam,</br><br></br><br></br>"+"A feedback report has been sent of student " + thesis.student.first_name + " " + thesis.student.last_name +'. Please Check the PhD Portal for more details.'+"<br></br><br></br>Regards,<br></br>PhDPortal."
        
        email = []

        for thesisGuide in ThesisGuide.objects.filter(thesis = thesis):
            receiver = Faculty.objects.get(user = thesisGuide.guide.user)
            email.append(receiver.email)

        send_email_task.delay(email, subject, content)
        return HttpResponse(json.dumps(dict), content_type = 'application/json')
    else:
        return redirect(reverse(URL_BAD_REQUEST))