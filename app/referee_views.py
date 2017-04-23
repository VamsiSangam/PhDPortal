from app.views import *
from app.director_views import invite_indian_referees
from app.director_views import invite_foreign_referees
import os
import shutil
from django.template import Context
from django.template.loader import get_template
from subprocess import check_output
import tempfile
import datetime
from datetime import time
from app.tasks import send_email_task

from app.tokens import PasswordResetTokenGenerator


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


def forgotpassword(request):
    """
    Forgot Pasword Module
    Send an OTP to the email and mobile
    """
    if request.method == 'GET':
        return render(request, 'app/other/forgot_password.html', {'title':'Forgot Password?',})
    elif request.method == 'POST':
        print('Entered')
        username = request.POST['username']
        #python -m pip install -U pip
        #pip install cryptography
        if User.objects.filter(username = username).exists():
            user = User.objects.get(username = username)
            if Referee.objects.filter(user = user).exists():
                referee = Referee.objects.get(user = user)
                #generate token
                passwordResetTokenGenerator = PasswordResetTokenGenerator()
                token = PasswordResetTokenGenerator.generate_token(passwordResetTokenGenerator, str(user.id))
                token = str(token.decode('utf-8'))
                print(token)
                #email to referee
                subject = "[Password Reset Link]"
                message = 'http:////localhost:8000//reset//token=//' + token
                print(message)
                content = "<br>Dear sir,</br><br></br><br></br>Link is: "+message+'. Please click on the link to change the credentials.'+"<br></br><br></br>Regards,<br></br>PhDPortal."
                email = []
                receiver = referee.user
                email.append(receiver.email)
                send_email_task.delay(email, subject, content)
                #redirect to same page with status to check your mail and click on activation link
                
                dict = {'status' : 'Done', 'message' : 'An Activation link has been sent to your mail-id'}
                return HttpResponse(json.dumps(dict), content_type = 'application/json')
            else:#given username is not valid to use this feature
                dict = {'status': 'Error', 'message' : 'You are not Authorized to change password'}
                return HttpResponse(json.dumps(dict), content_type = 'application/json')
        else:#given username is not valid to use this feature
            dict = {'status': 'Error', 'message' : 'Invalid Username, Try Again!'}
            return HttpResponse(json.dumps(dict), content_type = 'application/json')
    else:
        return redirect(reverse(URL_BAD_REQUEST))

def validate_password_reset_link(request, token):
    """
    Checks the validity of the reset link 
    corresponding to the given 'token' parameter.
    """
    print("reset")
    if request.method == "GET":
        print("reset")
        passwordResetTokenGenerator = PasswordResetTokenGenerator()
        id = PasswordResetTokenGenerator.get_token_value(passwordResetTokenGenerator, token)
        print(id)
        if id != None:
            id = int(id)

            if User.objects.filter(id = id).exists():
                user = User.objects.get(id = id)
                request.session['user'] = user.username
                print(request.session['user'])
                return render(request, 'app/referee/change_forgot_password.html', {
                'title':'Change Password',
                'user': user.username
                })
            else:##the user is invalid
                return redirect(reverse(URL_BAD_REQUEST))
        else:##either the link is expired or invalid
             return redirect(reverse(URL_BAD_REQUEST))
    else:##else --dont care
        return redirect(reverse(URL_BAD_REQUEST))

def referee_change_forgot_password(request):
   # if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))
    
    if request.method == 'POST':
        print("changing")
        username = request.POST['user']
        print(username + "********")
        user = User.objects.get(username = username)
        new = request.POST['new-password']
        re_type = request.POST['re-type']
        if new == re_type:
            user.set_password(new)
            user.save()
            dict = {'status' : 'Done', 'message' : 'Your password has been changed successfully' }
        else:
            dict = {'status' : 'Error-1', 'message' : 'Make sure that New password and Re-type fields are same' }

        return HttpResponse(json.dumps(dict), content_type = 'application/json')

    return redirect(reverse(URL_BAD_REQUEST))

@login_required
def referee_change_password(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))
    
    if request.method == 'GET':
        user = auth.get_user(request)
        #user_details = _get_user_type_object(user)
        
        return render(request, 'app/referee/change_password.html', {
                'title':'Change Password',
                'layout_data' : get_layout_data(request),
            })
    elif request.method == 'POST':
        user = auth.get_user(request)
        #user = _get_user_type_object(user)  # temporary fix
        old = request.POST['old-password']
        new = request.POST['new-password']
        re_type = request.POST['re-type']
        if user.check_password(old):
            if new == re_type:
                user.set_password(new)
                user.save()
                dict = {'status' : 'Done', 'message' : 'Your password has been changed successfully' }
            else:
                dict = {'status' : 'Error-1', 'message' : 'Make sure that New password and Re-type fields are same' }
        else:
            dict = {'status' : 'Error-2', 'message' : 'Make sure that the old password is correct' }

        return HttpResponse(json.dumps(dict), content_type = 'application/json')

    return redirect(reverse(URL_BAD_REQUEST))

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
        
        for panelMember in PanelMember.objects.filter(referee = referee).filter(status = 'S'):
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
        isApproved = (request.POST['isApproved'] == "True")
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
                invite_indian_referees(thesis)
            else:
                invite_foreign_referees(thesis)
        
        
        ############################################################################
        # notify guides & co-guides ---notify only admin and director
        #for thesisGuide in ThesisGuide.objects.filter(thesis = thesis):
        #    guide = thesisGuide.guide.user
        #    message = 'Referee ' + referee.user.first_name + ' ' + referee.user.last_name + ' '

        #    if isApproved:
        #        message += 'has approved to evaluate the PhD with title ' + thesis.title + '.'
        #    else:
        #        message += 'has rejected to evaluate the PhD with title ' + thesis.title + '.'

        #    if len(feedback.strip()) > 0:
        #        message += ' Referee has given the following feedback - ' + feedback

        #    send_notification(referee.user, guide, message, '')
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

    
    user = auth.get_user(request)
    referee = Referee.objects.get(user = user)
    
    if request.method == "GET":
        all_thesis = []     # list of dict
        
        for panelMember in PanelMember.objects.filter(referee = referee).filter(status = 'A'):
            thesis = panelMember.thesis
            dict = {}
            dict['title'] = thesis.title

            dict['student_full_name'] = thesis.student.first_name + ' ' + thesis.student.last_name
            dict['synopsis'] = thesis.synopsis
            dict['thesis'] = thesis.thesis
            dict['keywords'] = []
            for keys in ThesisKeyword.objects.filter(thesis = thesis):
                    dict['keywords'].append((IEEEKeyword.objects.get(id = keys.keyword.id)).keyword)
            
            dict['student_username'] = thesis.student.user.username
            dict['id'] = thesis.id
            
            all_thesis.append(dict)
        return render(
            request,
            'app/referee/evaluate_thesis.html',
            {
                'title':'Evaluate Thesis',
                'layout_data' : get_layout_data(request),
                'all_thesis' : all_thesis
            }
        )
    else:
        return redirect(reverse(URL_BAD_REQUEST))

#@login_required
#def convert_latex(request,user_template,context):
    
#    #tempdir = 'C:\\Users\\Sarada\\Documents' # move this to settings.py

#    template = get_template(user_template)
    
#    rendered_tpl = template.render(context).encode('utf-8')  
    
#    with tempfile.TemporaryDirectory() as tempdir:
#        shutil.copy(os.getcwd()+"\\texput.tex",tempdir)
#        shutil.copy(os.getcwd()+"\\logo.jpg",tempdir)
#        with open(tempdir + '/texput.tex', 'wb') as file_:
#            file_.write(rendered_tpl)
#        print("**************************************")
#        for i in range(2):
#            str = 'pdflatex -interaction=nonstopmode -output-directory=' + tempdir + ' ' + tempdir + '\\texput.tex'
#            print(str)
#            m = check_output(str)
#        print(os.listdir(tempdir))
#        with open(os.path.join(tempdir, 'texput.pdf'), 'rb') as f:
#            pdf = f.read()

#    #with open(tempdir + '/results2.tex', 'wb') as file_:
#    #    file_.write(rendered_tpl)
#    #print("**************************************")
#    #for i in range(2):
#    #    str = 'pdflatex -interaction=nonstopmode -output-directory=' + tempdir + ' ' + tempdir + '\\results2.tex'
#    #    print(str)
#    #    m = check_output(str)

#    #with open(os.path.join(tempdir, 'results2.pdf'), 'rb') as f:
#    #    pdf = f.read()
        
    
#   # r = HttpResponse(content_type='application/pdf')
    
#    #r['Content-Disposition'] = 'attachment; filename=raf.pdf'
#    #r.write(pdf)
#    #return pdf
#    return tempdir

_latex_special_chars = {
        u'$': u'\\$',
        u'%': u'\\%',
        u'&': u'\\&',
        u'#': u'\\#',
        u'_': u'\\_',
        #u'{': u'\\{',
        #u'}': u'\\}',
        #u'[': u'{[}',
        #u']': u'{]}',
        u'"': u"{''}",
        #u'\\': u'\\textbackslash{}',
        u'~': u'\\textasciitilde{}',
        u'<': u'\\textless{}',
        u'>': u'\\textgreater{}',
        u'^': u'\\textasciicircum{}',
        #    u'`':  u'{}`',   # avoid ?` and !`
        #    u'\n': u'\\\\',
        }


def text_escape(s):
    #s = s.encode('ascii', 'ignore')
    
    s = str(s)
    s = s.replace('"', '\'')
    #print(s)
    s = u''.join(_latex_special_chars.get(c, c) for c in s)
    return s
@login_required
def referee_thesis_approval(request):
    """
    Handles user request to approve/reject thesis document
    """

    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))
    
    user = auth.get_user(request)
    referee = Referee.objects.get(user = user)
    
    if request.method == "POST":
        
        id = int(request.POST['id'])
        thesis_organisation_get_up = request.POST['thesis-organisation-get-up']
        quality_check = request.POST['quality-check']
        orginal_check = request.POST['orginal-check']
        grammer_check = request.POST['grammer-check']
        thesis_technical_content = request.POST['thesis-technical-content']
        thesis_highlights_points = request.POST['thesis-highlights-points']
        
        IsReevaluation = False

        suggestions_check = request.POST['suggestions-check']
        
        if suggestions_check == '1':
            suggestions_check = 'Minor queries or suggestions or modifications to which the student replies in writing and which is communicated to the oral board together with my report.'
        else:
            suggestions_check = 'Suggestions and modifications to which the students written reposnse is sent to me. I will give my reply to the same in two weeks of its receipt. This is neccessary before the thesis is considered by the oral board.'
            IsReevaluation = True
        
        specific_recommendations = request.POST['specific-recommendations']

        if specific_recommendations == '1':
            specific_recommendations = 'Thesis is acceptable in the present form for the award of PhD degeree.'
        elif specific_recommendations == '2':
            specific_recommendations = 'The thesis is acceptable and the corrections, modifications, and improvement suggested by me would be incorporated in the thesis to the satisfaction of the oral board.'
        else:
            specific_recommendations = 'The thesis needs techincal improvement or modifications, which must be carried out to my satisfaction before I recomment this thesis for acceptance.'
            IsReevaluation = True
        
        feedback = request.POST['feedback']
       
        thesis = Thesis.objects.get(id = id)

        #studentdetails
        student = Student.objects.get(user = thesis.student.user)

        student_department = request.POST['Department']

        student_name = student.first_name + ' ' + student.middle_name + ' ' + student.last_name

        ##referee details
        student_id = student.current_roll_no
        
        student_username = student.user.username
        referee_name = referee.user.first_name + ' ' + referee.user.last_name
        referee_designation = referee.designation
        referee_university = referee.university
        referee_website = referee.website
        #need to be changed
        referee_ph_number = '+91-8935020870'
        referee_email = referee.user.email
        print(" ********* ")

        feedback = text_escape(feedback)
        thesis_organisation_get_up = text_escape(thesis_organisation_get_up)
        thesis_technical_content = text_escape(thesis_technical_content)
        thesis_highlights_points = text_escape(thesis_highlights_points)
        print(feedback)
        context = Context({
            'student_name': student_name,
            'student_id': student_id,
            'student_department': student_department,
            'referee_name': referee_name,
            'referee_designation': referee_designation,
            'referee_university': referee_university,
            'referee_website': referee_website,
            #need to be changed
            'referee_ph_number': referee_ph_number,
            'referee_email': referee_email,
            'feedback': feedback,
            'thesis_organisation_get_up': thesis_organisation_get_up,
            'quality_check': quality_check,
            'orginal_check': orginal_check,
            'grammer_check': grammer_check,
            'thesis_technical_content': thesis_technical_content,
            'thesis_highlights_points': thesis_highlights_points,
            'suggestions_check': suggestions_check,
            'specific_recommendations': specific_recommendations        
            })



        template = get_template('final_report.tex')
    
        rendered_tpl = template.render(context).encode('utf-8')  
    
        with tempfile.TemporaryDirectory() as tempdir:
            shutil.copy(os.getcwd()+"\\texput.tex",tempdir)
            shutil.copy(os.getcwd()+"\\logo.jpg",tempdir)
            with open(tempdir + '/texput.tex', 'wb') as file_:
                file_.write(rendered_tpl)
            print("**************************************")
            for i in range(2):
                m = check_output('xelatex -interaction=nonstopmode -output-directory=' + tempdir + ' ' + tempdir + '\\texput.tex')
            print(os.listdir(tempdir))
            with open(os.path.join(tempdir, 'texput.pdf'), 'rb') as f:
                pdf = f.read()
            #tempdir = convert_latex(request, 'final_report.tex',context)
            print(os.listdir(tempdir))
            print(" ********* ")
            panelmember = PanelMember.objects.get(thesis = thesis, referee = referee)
            print(" ********* ")
            if IsReevaluation:
                panelmember.status = 'Z'
            else:
                panelmember.status = 'F'
            time = str(datetime.datetime.now())
            timestamp = ''
            for i in time:
                if not (i == ':' or i == '-'):
                    timestamp += i
        
            print(" ********* " + timestamp + "**********")
            print()
            #tempdir = "C:\\Users\\Sarada\\Documents"
            shutil.copy(tempdir+"\\texput.pdf", os.getcwd() + "\\app\\static\\Feedback_With_Details\\"+ student_username + timestamp +".pdf")

            panelmember.feedback_with_referee_details = 'Feedback_With_Details\\' + student_username + timestamp + '.pdf'
            panelmember.save()
        
            ##without details
            template = get_template('final_report_without_details.tex')
    
            rendered_tpl = template.render(context).encode('utf-8')  
    
            with tempfile.TemporaryDirectory() as tempdir:
                shutil.copy(os.getcwd()+"\\texput.tex",tempdir)
                shutil.copy(os.getcwd()+"\\logo.jpg",tempdir)
                with open(tempdir + '/texput.tex', 'wb') as file_:
                    file_.write(rendered_tpl)
                print("**************************************")
                for i in range(2):
                    m = check_output('xelatex -interaction=nonstopmode -output-directory=' + tempdir + ' ' + tempdir + '\\texput.tex')
                print(os.listdir(tempdir))
                with open(os.path.join(tempdir, 'texput.pdf'), 'rb') as f:
                    pdf = f.read()
                #tempdir = convert_latex(request, 'final_report_without_details.tex',context)
                time =str(datetime.datetime.now())
                timestamp = ''
                for i in time:
                    if not (i == ':' or i == '-'):
                        timestamp += i
        
                print(" ********* " + timestamp + "**********")

                #tempdir = "C:\\Users\\Sarada\\Documents"
                shutil.copy(tempdir+"\\texput.pdf", os.getcwd() + "\\app\\static\\Feedback_Without_Details\\"+ student_username + timestamp +".pdf")

                panelmember.feedback_without_referee_details = 'Feedback_Without_Details\\' + student_username + timestamp + '.pdf'
                panelmember.save()
        
            message = 'A Feedback report of Thesis titled ' + thesis.title + ' has been sent'
            #notication to Admin
            admin = Admin.objects.all()
            email = []
            for admin in admin:
                send_notification(user, admin.user, message, '')
                email.append(admin.user.email)

        
            #Email to Admin
            subject = '[Feedback Report]'
            content = "<br>Dear sir,</br><br></br><br></br>"+ message + '. Please Check the PhD Portal for more details.'+"<br></br><br></br>Regards,<br></br>PhDPortal." 
            send_email_task.delay(email, subject, content)
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

    if request.method == "GET":
        return render(
            request,
            'app/referee/procedure.html',
            {
                'title':'Procedure',
                'layout_data' : get_layout_data(request),
            }
        )
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def referee_help_contacts(request):
    """
    View method. Renders page for contact help
    """

    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    if request.method == "GET":
        return render(
            request,
            'app/referee/help_contacts.html',
            {
                'title':'Help Contacts',
                'layout_data' : get_layout_data(request),
            }
        )
    else:
        return redirect(reverse(URL_BAD_REQUEST))