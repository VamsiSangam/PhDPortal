from app.views import *
from app.views import _get_user_type
from app.views import _clean_user_info_results

from app.student_views import _update_student_status
from django.db.models import Q
import os
import shutil
import datetime
from datetime import time, timedelta
from django.template import Context
from django.template.loader import get_template
from subprocess import check_output
import tempfile


from app.tasks import send_email_task

STATUS_ID_SUBMIT_ABSTRACT = 5
STATUS_ID_ABSTRACT_WAITING_APPROVAL = 6
STATUS_ID_ABSTRACT_APPROVED = 8
STATUS_ID_REQUEST_SPGC_TO_UPLOAD_SYNOPSIS = 9
STATUS_ID_REQUEST_PENDING_BY_SPGC_TO_UPLOAD_SYNOPSIS = 10
STATUS_ID_SUBMIT_SYNOPSIS = 11
STATUS_ID_SYNOPSIS_WAITING_APPROVAL = 12
STATUS_ID_SYNOPSIS_APPROVED = 14
STATUS_ID_PRE_SUBMISSION = 15
STATUS_ID_SUBMIT_THESIS = 16
STATUS_ID_THESIS_WAITING_APPROVAL = 17
STATUS_ID_THESIS_APPROVED = 19
STATUS_ID_WAITING_FOR_PANEL_APPROVAL = 20
STATUS_ID_PANEL_SENT = 21
STATUS_ID_WAITING_FOR_PANEL_APPROVAL_BY_ADMIN = 22
STATUS_ID_PANEL_SENT_TO_DIRECTOR = 23
STATUS_ID_WAITING_FOR_PANEL_APPROVAL_BY_DIRECTOR = 24
STATUS_ID_PANEL_SUBMITTED_BY_DIRECTOR = 25
STATUS_ID_THESIS_UNDER_EVALUATION = 26
STATUS_ID_THESIS_FEEDBACKS_RECEIVED = 27
STATUS_ID_ASKED_FOR_MODIFICATIONS = 28
STATUS_ID_CALL_FOR_VIVAVOICE = 29


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
    
    dict = {}
    if request.method == 'POST': 
        user_form = UserForm(request.POST)
        referee_form = RefereeForm(request.POST)
        email = request.POST['email']
        if user_form.is_valid() and referee_form.is_valid():
            if User.objects.filter(email = email).exists() == False :
                new_user = user_form.save(commit = False)
                new_user.is_active = True
                new_user.username = request.POST['email']
                passwd = 'HelloWorld'
                new_user.set_password(passwd)
                new_user.save()
                # to get added_by key
                new_referee = referee_form.save(commit = False)
                new_referee.isapproved = True
                new_referee.added_by = user
                new_referee.user = new_user
                new_referee.save()

                # send notification to that referee
                notify = "Hi sir/Madam! Welcome to the PhDPortal if IIIT-Allahabad.Please Update your Password"
                message = "You are added to the PhDPortal of IIIT-Allahabad.Please kindly check the Portal and update your Password.<br>Username is "+ str(request.POST.get('username')) + "<br>Password is" + passwd + "<br>"
                send_notification(user, new_user, notify, '')
                # email to referee
                subject = "[Invitation]"
                content = "<br>Dear sir,</br><br></br><br></br>"+message+'. Please Check the PhD Portal for more details.'+"<br></br><br></br>Regards,<br></br>PhDPortal."

                email = []
                receiver = new_user
                email.append(receiver.email)
                send_email_task.delay(email, subject, content)

                dict = {'status' : 'Done', 'message' : 'Added the referee Successfully!' }
            else :
                dict = {'status' : 'Not-Done', 'message' : 'Email-Id Already exists!' }
        else:
            dict = {'status' : 'Not-Done', 'message' : 'Fill the Fields appropriately!' }
            
    elif request.method == 'GET':
        user_form = UserForm()
        referee_form = RefereeForm()

    else:
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
        if Referee.objects.filter(user = referee, isapproved = False).exists():
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
        email = request.POST['email']
        if user_form.is_valid() and referee_form.is_valid():
            if User.objects.filter(email = email).exists() == False: 
                passwd = 'HelloWorld' # change this to customized timestamp
                existing_user.set_password(passwd)
                existing_user.username = email
                existing_user.is_active = True
                existing_referee.isapproved = True
                existing_user.save()
                user_form.save()
                referee_form.save()
            
                # send notification to that referee
                notify = "Hi sir/Madam! Welcome to the PhDPortal of IIIT-Allahabad.Please Update your Password."
                message = "You are added to the PhDPortal of IIIT-Allahabad.Please kindly check the Portal and update your Password.<br>Username is "+ str(request.POST.get('username')) + "<br>Password is" + passwd + "<br>"
                send_notification(user, existing_user, notify, '')
                # email to referee
                subject = "[Invitation]"
                content = "<br>Dear sir,</br><br></br><br></br>"+message+'. Please Check the PhD Portal for more details.'+"<br></br><br></br>Regards,<br></br>PhDPortal."

                email = []
                receiver = existing_user
                email.append(receiver.email)
                send_email_task.delay(email, subject, content)
            
                dict = {'status' : 'Done', 'message' : 'Added the referee Successfully!' }
            else:
                dict = {'status' : 'Not-Done', 'message' : 'Email-Id already exists!' }
        else:
            dict = {'status' : 'Not-Done', 'message' : 'Fill the Fields appropriately!' }
    
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
            all_thesis.append(dict)
        
        return render(request, 'app/admin/view_finalReports.html', {
            'title':'Final Reports',
            'layout_data' : get_layout_data(request),
            'all_thesis' : all_thesis
        })
    elif request.method == "POST":
        form = PanelMember2Form(request.POST, request.FILES)
        

        thesis = int(request.POST['thesis'])
        referee = int(request.POST['referee'])
        
        if form.is_valid() and validate_pdf(request.FILES['feedback_without_referee_details']):
            referee = Referee.objects.get(id = referee)
            thesis = Thesis.objects.get(id = thesis)
            panelmember = PanelMember.objects.get(thesis = thesis,referee = referee)
            panelmember.feedback_at = 'G'
            
            time = str(datetime.datetime.now())
            timestamp = ''
            for i in time:
                if not (i == ':' or i == '-'):
                    timestamp += i
            request.FILES['feedback_without_referee_details'].name = "Evaluation_Report_"+thesis.student.user.username+"_"+timestamp+".pdf"
           
            panelmember.feedback_without_referee_details = request.FILES['feedback_without_referee_details']
            panelmember.save()

            total_feedbacks = PanelMember.objects.filter(thesis = thesis, feedback_at = 'G').count()
            if total_feedbacks == thesis.indian_referees_required + thesis.foreign_referees_required:
                _update_student_status(thesis, STATUS_ID_THESIS_FEEDBACKS_RECEIVED) 

            # send notification to all guide
            send_notification_to_all_guides(admin, thesis, "A feedback report has been sent of student " + thesis.student.first_name + " " + thesis.student.last_name)
            # email
            subject = "[Feed Back reports] of the Thesis titled" + thesis.title
            content = "<br>Dear Sir/Madam,</br><br></br><br></br>"+"A feedback report has been sent of student " + thesis.student.first_name + " " + thesis.student.last_name +'. Please Check the PhD Portal for more details.'+"<br></br><br></br>Regards,<br></br>PhDPortal."
        
            email = []

            for thesisGuide in ThesisGuide.objects.filter(thesis = thesis):
                receiver = Faculty.objects.get(user = thesisGuide.guide.user)
                email.append(receiver.email)

            send_email_task.delay(email, subject, content)
            return redirect(reverse(admin_evaluate_reports))
        else:
            return redirect(reverse(URL_BAD_REQUEST))
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def admin_view_request_for_synopsis(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))
    
    user = auth.get_user(request)

    if request.method == "GET":
        all_thesis = []
        
        for thesis in Thesis.objects.all():
            if  thesis.status.id > STATUS_ID_REQUEST_SPGC_TO_UPLOAD_SYNOPSIS and thesis.status.id < STATUS_ID_SUBMIT_SYNOPSIS:
                dict = {}
                dict['title'] = thesis.title
                dict['student_full_name'] = thesis.student.first_name + ' ' + thesis.student.last_name
                dict['id'] = thesis.id
                all_thesis.append(dict)
        return render(
            request,
            'app/admin/approval_for_synopsis.html',
            {
                'title':'PhD Synopsis',
                'layout_data' : get_layout_data(request),
                'all_thesis' : all_thesis
            }
        )
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def admin_evaluate_request_for_synopsis(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))
    
    user = auth.get_user(request)

    if request.method == "POST":
        user = auth.get_user(request)
        thesisid = int(request.POST['id'])
        isGranted = (request.POST['isGranted'] == "True")
        feedback = request.POST['feedback']
        thesis = Thesis.objects.get(id = thesisid)
        
        if isGranted:
            notification_message = "Congratulations!You are allowed to upload the synopsis, as the credits are fulfilled."
            _update_student_status(thesis, STATUS_ID_SUBMIT_SYNOPSIS )
        else:
            notification_message = "You are not allowed to upload the synopsis, as the credits arent fulfilled."
            _update_student_status(thesis, STATUS_ID_REQUEST_SPGC_TO_UPLOAD_SYNOPSIS)
        # notify student about approval/rejection
        send_notification(user, thesis.student.user, notification_message, '')
        # email to student
        subject = "[Regarding Submission of Synopsis]"
        content = "<br>Dear Student,</br><br></br><br></br>"+notification_message+'. Please Check the PhD Portal for more details.'+"<br></br><br></br>Regards,<br></br>PhDPortal."

        email = []
        receiver = thesis.student.user
        email.append(receiver.email)
                    
        send_email_task.delay(email, subject, content)
        
        return HttpResponse('0', content_type = 'text/plain')
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def admin_preSubmissionSeminars(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))
    
    user = auth.get_user(request)

    if request.method == "GET":
        all_thesis = []
        
        for thesis in Thesis.objects.all():
            if  thesis.status.id >= STATUS_ID_PRE_SUBMISSION and thesis.status.id < STATUS_ID_SUBMIT_THESIS:
                dict = {}
                dict['title'] = thesis.title
                dict['student_full_name'] = thesis.student.first_name + ' ' + thesis.student.last_name
                dict['id'] = thesis.id
                dict['synopsis'] = thesis.synopsis
                all_thesis.append(dict)
        return render(
            request,
            'app/admin/pre_submission_seminar_approval.html',
            {
                'title':'PhD Pre-Submission Seminars',
                'layout_data' : get_layout_data(request),
                'all_thesis' : all_thesis
            }
        )
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def admin_preSubmissionSeminars_evaluate(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))
    
    user = auth.get_user(request)

    if request.method == "POST":
        user = auth.get_user(request)
        thesisid = int(request.POST['id'])
        isApproved = (request.POST['isApproved'] == "True")
        feedback = request.POST['feedback']
        thesis = Thesis.objects.get(id = thesisid)
        
        if isApproved:
            notification_message = "You are allowed to upload the thesis, as the open seminar is positive."
            _update_student_status(thesis, STATUS_ID_SUBMIT_THESIS )
        else:
            notification_message = "You are not allowed to upload the thesis, need the modified work and submit synopsis again."
            _update_student_status(thesis, STATUS_ID_SUBMIT_SYNOPSIS)

        # notify student about approval/rejection of seminar
        send_notification(user, thesis.student.user, notification_message, '')
        # email to student
        subject = "[Regarding PreSubmission seminar]"
        content = "<br>Dear Student,</br><br></br><br></br>"+notification_message+'. Please Check the PhD Portal for more details.'+"<br></br><br></br>Regards,<br></br>PhDPortal."

        email = []
        receiver = thesis.student.user
        email.append(receiver.email)
                    
        send_email_task.delay(email, subject, content)

        return HttpResponse('0', content_type = 'text/plain')
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def admin_panel_upload(request, id):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    if request.method == "POST":
        form = PanelListSignedCopyForm(request.POST, request.FILES)
       
        if form.is_valid() and validate_pdf(request.FILES['panel_signed_copy']):
            thesis = Thesis.objects.get(id = id)    
            time = str(datetime.datetime.now())
            timestamp = ''
            for i in time:
                if not (i == ':' or i == '-'):
                    timestamp += i
            request.FILES['panel_signed_copy'].name = "signed_copy_"+thesis.student.user.username+"_"+timestamp+".pdf"
            thesis.panel_signed_copy = request.FILES['panel_signed_copy']
            thesis.save()
            _update_student_status(thesis, STATUS_ID_WAITING_FOR_PANEL_APPROVAL_BY_DIRECTOR)
            return redirect(reverse('admin_panelapproval'))
        else:
            return redirect(reverse(URL_BAD_REQUEST))
    else:
        return redirect(reverse(URL_BAD_REQUEST))


@login_required
def admin_panelapproval(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))
    
    user = auth.get_user(request)

    if request.method == "GET":
        all_thesis = []     # list of dict
        
        for thesis in Thesis.objects.all():
            if  thesis.status.id >= STATUS_ID_PANEL_SENT and thesis.status.id < STATUS_ID_PANEL_SENT_TO_DIRECTOR:
                dict = {}
                dict['guides'] = []
                for thesisGuides in ThesisGuide.objects.filter(thesis = thesis):
                    guide = {}
                    guide['fullname'] = thesisGuides.guide.first_name + " " + thesisGuides.guide.middle_name + " " + thesisGuides.guide.last_name
                    if thesisGuides.type == 'G':
                        guide['type'] = 'Guide'
                    else:
                        guide['type'] = 'Co-Guide'
                    dict['guides'].append(guide)
                dict['title'] = thesis.title
                dict['student_full_name'] = thesis.student.first_name + ' ' + thesis.student.last_name
                dict['id'] = thesis.id
                dict['thesis'] = thesis.thesis
                all_thesis.append(dict)
        return render(
            request,
            'app/admin/panel_approval.html',
            {
                'title':'PhD Pre-Submission Seminars',
                'layout_data' : get_layout_data(request),
                'all_thesis' : all_thesis
            }
        )
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def admin_panelapproval_evaluate(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))
    
    user = auth.get_user(request)

    if request.method == "POST":
        
        user = auth.get_user(request)
        thesisid = int(request.POST['id'])
        isApproved = (request.POST['isApproved'] == "True")
        feedback = request.POST['feedback']
        thesis = Thesis.objects.get(id = thesisid)
        
        if isApproved:
            _update_student_status(thesis, STATUS_ID_WAITING_FOR_PANEL_APPROVAL_BY_DIRECTOR)    
        else:
            for thesisGuides in ThesisGuide.objects.filter(thesis = thesis):
                guide = thesisGuides.guide
                allReferees = PanelMember.objects.filter(thesis = thesis).filter(added_by = guide, status = 'G')
                for referee in allReferees:
                    referee.status = 'D'
                    referee.save()
            _update_student_status(thesis, STATUS_ID_WAITING_FOR_PANEL_APPROVAL)

        return HttpResponse('0', content_type = 'text/plain')
    else:
        return redirect(reverse(URL_BAD_REQUEST))

    
@login_required
def admin_panel_print(request,id):
    thesis = Thesis.objects.get(id = id)
    indian_referees = []
    foreign_referees = []
    indian_referees_university = []
    foreign_referees_university = []
            
    for member in PanelMember.objects.filter(thesis = thesis,status = 'G'):
        referee = Referee.objects.get(id = member.referee.id)
        ref = User.objects.get(id = member.referee.user.id)
        name = ref.first_name + ' ' +ref.last_name
        university = referee.university
        if referee.type == 'I':
            dict = {}
            dict['name'] = name
            dict['university'] = university
            indian_referees.append(dict)
        else:
            dict = {}
            dict['name'] = name
            dict['university'] = university
            foreign_referees.append(dict)

    context = Context({
        'student_name': 'shanu',
        'indian_referees' : indian_referees,
        'foreign_referees' : foreign_referees,
        })

    template = get_template('panel.tex')
    rendered_tpl = template.render(context).encode('utf-8')  
    
    with tempfile.TemporaryDirectory() as tempdir:
        shutil.copy(os.getcwd()+"\\texput.tex",tempdir)
        shutil.copy(os.getcwd()+"\\logo.jpg",tempdir)
        
        with open(tempdir + '/texput.tex', 'wb') as file_:
            file_.write(rendered_tpl)

        for i in range(2):
            m = check_output('xelatex -interaction=nonstopmode -output-directory=' + tempdir + ' ' + tempdir + '\\texput.tex')
        
        with open(os.path.join(tempdir, 'texput.pdf'), 'rb') as f:
            pdf = f.read()

    r = HttpResponse(content_type = 'application/pdf')
    r['Content-Disposition'] = 'attachement;filename = panel_list.pdf'
    r.write(pdf)

    return r

@login_required
def admin_conductSeminar(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))
    
    user = auth.get_user(request)
    
    if request.method == "POST":
        thesis = Thesis.objects.get(id = int(request.POST['id']))
        student_name = thesis.student.first_name + " " + thesis.student.last_name
        # send notifications
        notification_message = "It is agreed to conduct the presubmission seminar of the student " +  student_name
        notification_message += ' for the PhD titled "' + thesis.title + '"'
        for thesisGuide in ThesisGuide.objects.filter(thesis = thesis):
            send_notification(user, thesisGuide.guide.user, notification_message, '')
        
        subject = "[Conducting Open seminar] of " + request.session['full_name']
        content = "<br>Dear Sir/Madam,</br><br></br><br></br>"+notification_message+'.Please Check the PhD Portal for more details.'+"<br></br><br></br>Regards,<br></br>DUPGC."
        email = []

        for thesisGuide in ThesisGuide.objects.filter(thesis = thesis):
            receiver = Faculty.objects.get(user = thesisGuide.guide.user)
            email.append(receiver.email)

        send_email_task.delay(email, subject, content)

        dict = {'status' : 'OK', 'message' : 'Successfully Notified the guides!'}
        return HttpResponse(json.dumps(dict), content_type = 'application/json')
    else:
        return redirect(reverse(URL_BAD_REQUEST))



@login_required
def admin_search_student(request):
    """
    View method. Renders a search utility to search for admin.
    """

    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))
    if request.session['type'] == 'S' or request.session['type'] == 'R': return redirect(reverse(URL_FORBIDDEN))

    if request.method == "GET":
        return render(
            request,
            'app/admin/admin_search_student.html',
            {
                'title':'Student Info',
                'layout_data' : get_layout_data(request),
            }
        )
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def admin_search_student_query(request):
    """
    Handles an AJAX request from the search admin view

    Returns:
        Top 15 search results in JSON format.
    """

    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))
    if request.session['type'] == 'S' or request.session['type'] == 'R': return redirect(reverse(URL_FORBIDDEN))

    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        type = request.POST['type']
        dict = {}

        for user in User.objects.all():
            user_type = _get_user_type(user)

            if user_type is None or user_type == 'A':
                continue    # for user who are not S, G, F, D, R, A

            user_first_name = None
            user_last_name = None
            user_email = None
            
            votes = 0

            if user_type == type:
                votes += 2

            if user_type == 'S':
                user_first_name = user.student.first_name
                user_last_name = user.student.last_name
                user_email = user.student.email
            elif user_type == 'G' or user_type == 'D':
                user_first_name = user.faculty.first_name
                user_last_name = user.faculty.last_name
                user_email = user.faculty.email
            elif user_type == 'R':
                user_first_name = user.first_name
                user_last_name = user.last_name
                user_email = user.email

            if first_name.upper() in user_first_name.upper():
                votes += 1

            if last_name.upper() in user_last_name.upper():
                votes += 1

            if email.upper() in user_email.upper():
                votes += 1

            dict[user] = votes
        
        sorted_results = sorted(dict.items(), key = operator.itemgetter(1))
        sorted_results.reverse()
        result = _clean_user_info_results(sorted_results)

        return HttpResponse(json.dumps(result), content_type = 'application/json')
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def admin_student_refresh(request,id):
    thesis = Thesis.objects.get(id = id)

    if request.method == "GET":
        ThesisGuideApproval.objects.filter(thesis = thesis).delete()
        PanelMember.objects.filter(thesis = thesis).delete()
        ThesisKeyword.objects.filter(thesis = thesis).delete()
        CustomKeyword.objects.filter(thesis = thesis).delete()
        ThesisGuide.objects.filter(thesis = thesis).delete()
        thesis.abstract = ''
        thesis.thesis_modifications = ''
        thesis.panel_signed_copy = ''
        thesis.synopsis = ''
        thesis.thesis = ''
        
        status_type = StatusType.objects.get(id = 1)
        thesis.status = status_type
        thesis.save()
        

    return redirect(reverse('admin_search_student'))