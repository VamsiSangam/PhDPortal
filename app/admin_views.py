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

