from app.views import *
import datetime
from datetime import time, timedelta
from django.utils.datastructures import MultiValueDictKeyError
from app.tasks import send_email_task
from enchant.checker import SpellChecker
import os
import shutil
from django.template import Context
from django.template.loader import get_template
from subprocess import check_output
import tempfile


URL_STUDENT_ADD_ABSTRACT = 'student_add_abstract'
URL_STUDENT_VIEW_THESIS = 'student_view_thesis'
URL_STUDENT_ADD_KEYWORDS = 'student_add_keywords'
URL_STUDENT_ADD_DETAILS = 'student_add_details'

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

def send_notification_to_guides(user, message):
    """
    Sends a notification with given 'message' to
    all the guides mentoring given 'student'
    TODO: Notification model has link column which is still left un-utilized

    Args:
        user: User model object (of corresponding student)
        message: string object
    """
    student = Student.objects.get(user = user)
    thesis = Thesis.objects.get(student = student)

    for thesisGuide in ThesisGuide.objects.filter(thesis = thesis):
        receiver = User.objects.get(username = thesisGuide.guide.user.username)
        send_notification(user, receiver, message, '')

def _update_student_status(thesis, check_status_id):
    """
    Updates a student's phd status. Given a new value
    it checks if the existing value is equal to new value
    and then updates accordingly

    Args:
        thesis : Thesis model object
        check_status_id : int, a status id
    """
    
    thesis_status_id = thesis.status.id

    if thesis_status_id != check_status_id:
        status_type = StatusType.objects.get(id = check_status_id)
        thesis.status = status_type
        thesis.save()


@login_required
def student_add_details(request):
    """
    View method. Renders a page where student can submit PhD abstract
    """
    
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))
    
    user = auth.get_user(request)
    student = Student.objects.get(user = user)
    thesis = Thesis.objects.get(student = student)
    isDetailsApproved = (thesis.status.id >= STATUS_ID_SUBMIT_ABSTRACT)

    if request.method == "GET":
        dict = {'status' : 'get', 'message' : 'Please Provide the Title!'}

        return render(request, 'app/student/phd_add_details.html', {
            'layout_data' : get_layout_data(request),
            'isDetailsApproved' : isDetailsApproved,
            'dict': dict 
        })
    elif request.method == "POST" and (not isDetailsApproved):
        title = request.POST['title']
        guides = request.POST.getlist('guides[]')
        co_guides = request.POST.getlist('co_guides[]')
        
        isrepeat = False
        for guide in guides:
            for coguide in co_guides:
                if int(guide) == int(coguide):
                    dict = {'status' : 'nope', 'message' : 'Please Update The Details Properly According to the rules!'}
                    return HttpResponse(json.dumps(dict), content_type = 'application/json')

        guide_count = 0
        co_guide_count = 0
        for guide in guides:
            guide_count = guide_count + 1
        for co_guide in co_guides:
            co_guide_count = co_guide_count + 1
        if str(len(title)) == '0':
            dict = {'status' : 'nope', 'message' : 'Please Provide the Title!'}
        elif guide_count < 1:
            dict = {'status' : 'nope', 'message' : 'Please Update The Details Properly According to the rules!'}
        else :

            thesis.title = title
            thesis.save()
            
            for guide in guides:
                guide = Faculty.objects.get(id = int(guide))
                ThesisGuide(thesis = thesis, guide = guide, type = 'G').save()
            
            for co_guide in co_guides:
                guide = Faculty.objects.get(id = int(co_guide))
                ThesisGuide(thesis = thesis, guide = guide, type = 'C').save()
            
            _update_student_status(thesis, STATUS_ID_SUBMIT_ABSTRACT)
            dict = {'status' : 'OK', 'message' : 'Details Added Successfully!'}


        return HttpResponse(json.dumps(dict), content_type = 'application/json')

    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def student_add_abstract(request):
    """
    View method. Renders a page where student can submit PhD abstract
    """
    
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))
    
    user = auth.get_user(request)
    student = Student.objects.get(user = user)
    thesis = Thesis.objects.get(student = student)
    canSubmitAbstract = thesis.status.id >= STATUS_ID_SUBMIT_ABSTRACT
    abstractWaitingApproval = thesis.status.id > STATUS_ID_SUBMIT_ABSTRACT and thesis.status.id < STATUS_ID_ABSTRACT_APPROVED
    isAbstractApproved = thesis.status.id >= STATUS_ID_ABSTRACT_APPROVED

    if request.method == "GET":
        abstract = thesis.abstract

        return render(request, 'app/student/phd_abstract.html', {
            'title' : 'PhD Abstract',
            'layout_data' : get_layout_data(request),
            'abstract' : abstract,
            'canSubmitAbstract' : canSubmitAbstract,
            'isAbstractApproved' : isAbstractApproved,
            'abstractWaitingApproval' : abstractWaitingApproval
        })
    elif request.method == "POST" and canSubmitAbstract and (not isAbstractApproved):
        abstract = request.POST['abstract']
        thesis.abstract = abstract
        thesis.save()

        notification_message = 'Student ' + request.session['full_name'] + ' has submitted their PhD abstract '
        notification_message += 'for the PhD titled "' + thesis.title + '"'
        send_notification_to_guides(user, notification_message)
        # Email Notification
        subject = "[Abstract Submitted] by " + request.session['full_name']
        content = "<br>Dear Sir/Madam,</br><br></br><br></br>"+notification_message+'.Please Check the PhD Portal for more details.'+"<br></br><br></br>Regards,<br></br>DUPGC."
        
        student = Student.objects.get(user = user)

        thesis = Thesis.objects.get(student = student)
        email = []

        for thesisGuide in ThesisGuide.objects.filter(thesis = thesis):
            receiver = Faculty.objects.get(user = thesisGuide.guide.user)
            email.append(receiver.email)

        send_email_task.delay(email, subject, content)
        
        _update_student_status(thesis, STATUS_ID_ABSTRACT_WAITING_APPROVAL)
        
        return redirect(reverse(URL_STUDENT_ADD_ABSTRACT)) 
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def student_request_synopsis(request):
    """
    Handles and POST AJAX request -> student requests admin to
    grant permission to upload synopsis
    """
    
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))
    
    user = auth.get_user(request)
    student = Student.objects.get(user = user)
    thesis = Thesis.objects.get(student = student)
   
    
    if request.method == 'POST':
        _update_student_status(thesis, STATUS_ID_REQUEST_PENDING_BY_SPGC_TO_UPLOAD_SYNOPSIS)
        # notify admin to give permission to upload synopsis
        admin = Admin.objects.all()[0]
        notify = "Respected Sir/Madam! Please grant me the permission to upload the synopsis on portal."
        send_notification(user, admin.user, notify, '')
        # email to referee
        subject = "[Requesting permission to Upload synopsis]"
        content = "<br>Dear sir,</br><br></br><br></br>"+notify+'. Please Check the PhD Portal for more details.'+"<br></br><br></br>Regards,<br></br>"+ student.first_name+ " " + student.last_name

        email = []
        receiver = admin.user
        email.append(receiver.email)
        send_email_task.delay(email, subject, content)

        return redirect(reverse('student_upload_synopsis'))    
    else:
        return redirect(reverse(URL_BAD_REQUEST))


@login_required
def student_upload_synopsis(request):
    """
    View method. Renders a page where student can submit PhD synopsis
    """
    
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))
    
    user = auth.get_user(request)
    student = Student.objects.get(user = user)
    thesis = Thesis.objects.get(student = student)
   
    isAbstaractApproved = thesis.status.id >= STATUS_ID_REQUEST_SPGC_TO_UPLOAD_SYNOPSIS
    canRequestSynopsis = thesis.status.id == STATUS_ID_REQUEST_SPGC_TO_UPLOAD_SYNOPSIS
    requestWaitingApproval = thesis.status.id > STATUS_ID_REQUEST_SPGC_TO_UPLOAD_SYNOPSIS and thesis.status.id < STATUS_ID_SUBMIT_SYNOPSIS
    canSubmitSynopsis = thesis.status.id >= (STATUS_ID_SUBMIT_SYNOPSIS)
    synopsisWaitingApproval = thesis.status.id > STATUS_ID_SUBMIT_SYNOPSIS and thesis.status.id < STATUS_ID_SYNOPSIS_APPROVED
    isSynopsisApproved = thesis.status.id >= STATUS_ID_SYNOPSIS_APPROVED
    canCancelSynosis = thesis.status.id == STATUS_ID_SYNOPSIS_WAITING_APPROVAL

    if request.method == 'GET':
        return render(
            request,
            'app/student/upload_synopsis.html',
            {   
                'title' : 'Upload Synopsis',
                'layout_data' : get_layout_data(request),
                'isAbstaractApproved' : isAbstaractApproved,
                'canRequestSynopsis' : canRequestSynopsis,
                'requestWaitingApproval' : requestWaitingApproval,
                'canSubmitSynopsis' : canSubmitSynopsis,
                'canCancelSynosis' : canCancelSynosis,
                'isSynopsisApproved' : isSynopsisApproved,
                'synopsisWaitingApproval' : synopsisWaitingApproval
            }
        )
    elif request.method == "POST" and canSubmitSynopsis and (not isSynopsisApproved):
        form = SynopsisForm(request.POST, request.FILES)
        
        if form.is_valid() and validate_pdf(request.FILES['synopsis']):
            time = str(datetime.datetime.now())
            timestamp = ''
            for i in time:
                if not (i == ':' or i == '-'):
                    timestamp += i
            request.FILES['synopsis'].name = user.username+"_synopsis_"+timestamp+".pdf"
            thesis.synopsis = request.FILES['synopsis']
            thesis.save()

            notification_message = 'Student ' + request.session['full_name'] + ' has submitted their PhD synopsis '
            notification_message += 'for the PhD titled "' + thesis.title + '"'
            send_notification_to_guides(user, notification_message)
            subject = "[Synopsis Submitted] by " + request.session['full_name']
            content = "<br>Dear Sir/Madam,</br><br></br><br></br>"+notification_message+'. Please Check the PhD Portal for more details.'+"<br></br><br></br>Regards,<br></br>PhDPortal."
        
            student = Student.objects.get(user = user)

            thesis = Thesis.objects.get(student = student)
            email = []

            for thesisGuide in ThesisGuide.objects.filter(thesis = thesis):
                receiver = Faculty.objects.get(user = thesisGuide.guide.user)
                email.append(receiver.email)

            send_email_task.delay(email, subject, content)
            _update_student_status(thesis, STATUS_ID_SYNOPSIS_WAITING_APPROVAL)

            return redirect(reverse('student_view_synopsis'))
        else:
            return redirect(reverse(URL_BAD_REQUEST))
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def student_view_synopsis(request):
    """
    View method. Renders a page to view student's uploaded synopsis.
    """

    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    if request.method == "GET":
        user = auth.get_user(request)
        student = Student.objects.get(user = user)
        thesis = Thesis.objects.get(student = student)
        synopsisPath = None

        if thesis.synopsis:
            synopsisPath = thesis.synopsis

        return render(
            request,
            'app/student/view_synopsis.html',
            {
                'title':'View Synopsis',
                'layout_data' : get_layout_data(request),
                'synopsisPath' : synopsisPath
            }
        )
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def student_upload_thesis(request):
    """
    View method. Renders a page for student to upload thesis document.
    """
    
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))
    
    user = auth.get_user(request)
    student = Student.objects.get(user = user)
    thesis = Thesis.objects.get(student = student)
    canSubmitThesis = thesis.status.id >= STATUS_ID_SUBMIT_THESIS 
    canReSubmitThesis = (thesis.status.id == STATUS_ID_ASKED_FOR_MODIFICATIONS)
    isThesisApproved = thesis.status.id >= STATUS_ID_THESIS_APPROVED
    thesisWaitingApproval = thesis.status.id > STATUS_ID_SUBMIT_THESIS and thesis.status.id < STATUS_ID_THESIS_APPROVED

    if request.method == "GET":
        thesisExists = bool(thesis.thesis)

        return render(
            request,
            'app/student/upload_thesis.html',
            {
                'title':'Upload Thesis',
                'layout_data' : get_layout_data(request),
                'thesisExists' : thesisExists,
                'canSubmitThesis' : canSubmitThesis,
                'canReSubmitThesis' : canReSubmitThesis,
                'isThesisApproved' : isThesisApproved,
                'thesisWaitingApproval' : thesisWaitingApproval
            }
        )
    elif request.method == "POST" and canSubmitThesis and (not isThesisApproved):
        form = ThesisForm(request.POST, request.FILES)
        isModifications = True
        isPdf = False
        try:
            modifications_file = request.FILES['thesis_modifications']
            isModifications = validate_pdf(modifications_file)
            isPdf = True
        except MultiValueDictKeyError:
            isModifications = True
       
        if form.is_valid() and validate_pdf(request.FILES['thesis']) and isModifications == True:   
            time = str(datetime.datetime.now())
            timestamp = ''
            for i in time:
                if not (i == ':' or i == '-'):
                    timestamp += i
            request.FILES['thesis'].name = user.username+"_thesis_"+timestamp+".pdf"
            thesis.thesis = request.FILES['thesis']
            if isPdf == True:
                request.FILES['thesis_modifications'].name = user.username+"_thesismodify_"+timestamp+".pdf"
                thesis.thesis_modifications = request.FILES['thesis_modifications']
            else:
                thesis.thesis_modifications = 'NULL'
            thesis.save()

            notification_message = 'Student ' + request.session['full_name'] + ' has submitted their PhD thesis document '
            notification_message += 'for the PhD titled "' + thesis.title + '"'
            send_notification_to_guides(user, notification_message)
            # Email Notification
            subject = "[Thesis Submitted] by " + request.session['full_name']
            content = "<br>Dear Sir/Madam,</br><br></br><br></br>"+notification_message+'. Please Check the PhD Portal for more details.'+"<br></br><br></br>Regards,<br></br>PhDPortal."
        
            student = Student.objects.get(user = user)

            thesis = Thesis.objects.get(student = student)
            email = []

            for thesisGuide in ThesisGuide.objects.filter(thesis = thesis):
                receiver = Faculty.objects.get(user = thesisGuide.guide.user)
                email.append(receiver.email)

            send_email_task.delay(email, subject, content)
            _update_student_status(thesis, STATUS_ID_THESIS_WAITING_APPROVAL)

            return redirect(reverse(URL_STUDENT_VIEW_THESIS))
        else:
            return redirect(reverse(URL_BAD_REQUEST))
    elif request.method == "POST" and canReSubmitThesis:
        form = ThesisForm(request.POST, request.FILES)
        isModifications = True
        isPdf = False
        
        try:
            modifications_file = request.FILES['thesis_modifications']
            isModifications = validate_pdf(modifications_file)
            isPdf = True
        except MultiValueDictKeyError:
            isModifications = True

        if form.is_valid() and validate_pdf(request.FILES['thesis']) and isModifications == True:    
            time = str(datetime.datetime.now())
            timestamp = ''
            for i in time:
                if not (i == ':' or i == '-'):
                    timestamp += i
            request.FILES['thesis'].name = user.username+"_thesis_"+timestamp+".pdf"
            thesis.thesis = request.FILES['thesis']
            thesis.save()
            
            if isPdf == True:
                request.FILES['thesis_modifications'].name = user.username+"_thesismodify_"+timestamp+".pdf"
                for panelmember in PanelMember.objects.filter(thesis = thesis, status = 'Z'):
                    panelmember.answer_for_questions = True
                    panelmember.save()
                thesis.thesis_modifications = request.FILES['thesis_modifications']
                
            else:
                for panelmember in PanelMember.objects.filter(thesis = thesis, status = 'Z'):
                    panelmember.answer_for_questions = False
                    panelmember.save()
                thesis.thesis_modifications = 'NULL'
            thesis.save()
            
            notification_message = 'Student ' + request.session['full_name'] + ' has Re-submitted their PhD thesis document after modifications'
            notification_message += 'for the PhD titled "' + thesis.title + '"'
            send_notification_to_guides(user, notification_message)
            # Email Notification
            subject = "[Thesis Submitted] by " + request.session['full_name']
            content = "<br>Dear Sir/Madam,</br><br></br><br></br>"+notification_message+'. Please Check the PhD Portal for more details.'+"<br></br><br></br>Regards,<br></br>PhDPortal."
        
            student = Student.objects.get(user = user)

            thesis = Thesis.objects.get(student = student)
            email = []

            for thesisGuide in ThesisGuide.objects.filter(thesis = thesis):
                receiver = Faculty.objects.get(user = thesisGuide.guide.user)
                email.append(receiver.email)

            send_email_task.delay(email, subject, content)
            _update_student_status(thesis, STATUS_ID_THESIS_FEEDBACKS_RECEIVED)

            return redirect(reverse(URL_STUDENT_VIEW_THESIS))
        else:
            return redirect(reverse(URL_BAD_REQUEST))
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def student_view_thesis(request):
    """
    View method. Renders a page to view student's uploaded thesis document
    """

    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    if request.method == "GET":
        user = auth.get_user(request)
        student = Student.objects.get(user = user)
        thesis = Thesis.objects.get(student = student)
        thesisPath = None

        if thesis.thesis:
            thesisPath = thesis.thesis

        return render(
            request,
            'app/student/view_thesis.html',
            {
                'title':'View Thesis',
                'layout_data' : get_layout_data(request),
                'thesisPath' : thesisPath
            }
        )
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def student_add_keywords(request):
    """
    View method. Renders a page which allows student to add keywords to PhD thesis
    """

    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    if request.method == "GET":
        user = auth.get_user(request)
        student = Student.objects.get(user = user)
        thesis = Thesis.objects.get(student = student)
        thesis_keywords = ThesisKeyword.objects.filter(thesis = thesis)
        custom_keywords = CustomKeyword.objects.filter(thesis = thesis)
        return render(
            request,
            'app/student/add_keywords.html',
            {
                'title':'Add Keywords',
                'layout_data' : get_layout_data(request),
                'thesis' : thesis,
                'STATUS_ID_THESIS_APPROVED' : STATUS_ID_THESIS_APPROVED,
                'STATUS_ID_SUBMIT_SYNOPSIS' : STATUS_ID_SUBMIT_SYNOPSIS,
                'thesis_keywords' : thesis_keywords,
                'custom_keywords' : custom_keywords
            }
        )
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def student_search_keywords(request):
    """
    Handles an AJAX request for keyword search
    For better User interface
    """

    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    if request.method == "POST":
        keyword_typed = request.POST['keyword-typed']
        keywords = IEEEKeyword.objects.filter(keyword__icontains = keyword_typed)

        
        result = _ieee_keywords_to_list(keywords)

        return HttpResponse(json.dumps(result), content_type = 'application/json')
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def student_keyword_recommendations(request):
    """
    Handles AJAX request to load a student's recommended keywords

    Displays the recommended keywords and it isn't the scope of this project 
    """
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    if request.method == "POST":
        keywords = IEEEKeyword.objects.filter(keyword__icontains = 'process')

        result = _ieee_keywords_to_list(keywords)

        return HttpResponse(json.dumps(result), content_type = 'application/json')
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def student_add_custom_keyword(request):
    """
    Handles AJAX request to add a custom keyword.
    """

    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    if request.method == "POST":
        keyword = request.POST['keyword']
        user = auth.get_user(request)
        student = Student.objects.get(user = user)
        thesis = Thesis.objects.get(student = student)

        chkr = SpellChecker("en_US")
        
        chkr.set_text(keyword)
        
        iserror = False

        if keyword == '':
            iserror = True

        for err in chkr:
            iserror = True

        if iserror == True:
            result = {'message' : 'Error! Please check the spelling once again!!'}
        else:
            custom = CustomKeyword(thesis = thesis, keyword = keyword)
            custom.save()
            result = {'message' : 'Success! Added the keyword to your thesis!!'}

        return HttpResponse(json.dumps(result), content_type = 'application/json')
    else:
        return redirect(reverse(URL_BAD_REQUEST))


def _validate_keyword(id, user):
    """
    Validates a thesis keyword. Used while deleting keyword.

    Args:
        id : int, id in ThesisKeyword model
        user : User object model

    Returns:
        True : if id matches with user's thesis
        False : if match fails
    """

    thesis_keyword = ThesisKeyword.objects.get(id = id)

    if thesis_keyword is not None:
        if thesis_keyword.thesis.student.user == user:
            return True

    return False

@login_required
def student_delete_keyword(request, id):
    """
    Handles a user request to delete a thesis keyword.
    Verifies the validity of id and deletes it.

    Args:
        id: id in ThesisKeywords model
    """
    
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))
    
    if request.method == "POST":
        
        try:
            custom_keyword = request.POST['custom_keyword']
            user = auth.get_user(request)
            for keyword in CustomKeyword.objects.filter(keyword = custom_keyword):
                if keyword.thesis.student.user == user:
                    keyword.delete()
            return redirect(reverse(URL_STUDENT_ADD_KEYWORDS))
        except MultiValueDictKeyError:
            simply = 1
        

        if _validate_keyword(id, auth.get_user(request)):
            
            thesis_keyword = ThesisKeyword.objects.get(id = id)
            thesis_keyword.delete()

            return redirect(reverse(URL_STUDENT_ADD_KEYWORDS))
        else:
            return redirect(reverse(URL_FORBIDDEN))
    else:
        return redirect(reverse(URL_BAD_REQUEST))

def _ieee_keywords_to_list(keywords):
    """
    Given a 'keyword', returns all the IEEEKeywords
    whose parent keyword is the input 'keyword'

    Args:
        keywords: IEEEKeyword query set

    Returns:
        list of dict, where each dict has the keys -
        'id', 'keyword', 'subkeywords', 'parent'
    """
    
    list = []

    for keyword in keywords:
        dict = {}
        dict['id'] = keyword.id
        dict['keyword'] = keyword.keyword
        dict['subkeywords'] = IEEEKeyword.objects.filter(parent = keyword).count()

        if keyword.parent is not None:
            dict['parent'] = keyword.parent.id

        list.append(dict)

    return list

@login_required
def get_ieee_keywords(request):
    """
    Handles a user request which fetches all
    keywords for a given parent keyword, outputs JSON
    TODO : change view to use 'parent' instead of 'parent_id'
    """
    
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    if request.method == "POST":
        parent = int(request.POST['parent'])
        keywords = None
        
        if parent == -1:
            keywords = IEEEKeyword.objects.filter(parent = None)
        else:
            parent_keyword = IEEEKeyword.objects.get(id = parent)

            if parent_keyword is not None:
                keywords = IEEEKeyword.objects.filter(parent = parent_keyword)
            else:
                return redirect(reverse(URL_UNAUTHORIZED_ACCESS))
        
        result = _ieee_keywords_to_list(keywords)

        # add parent to result, if present -> this is used to create 'Go back' link
        if parent != -1:
            parent_keyword = IEEEKeyword.objects.get(id = parent)
            parent_keyword = parent_keyword.parent
            dict = {}

            if parent_keyword is not None:
                dict = {'id' : parent_keyword.id, 'keyword' : 'Go back to ' + parent_keyword.keyword }
            else:
                dict = {'id' : -1, 'keyword' : 'Go back '}

            result.append(dict)

        return HttpResponse(json.dumps(result), content_type = 'application/json')
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def get_ieee_keywords_parent(request):
    """
    handles a user request for getting the parent id of an IEEEKeyword.
    Outputs in text/plain.
    """

    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))
    
    if (request.method == "POST"):
        keyword = IEEEKeyword.objects.get(id = request.POST['parent_id'])
        id = keyword.parent.id

        if id is None:
            id = -1

        return HttpResponse(id, content_type = 'text/plain')
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def student_add_keyword_to_thesis(request):
    """
    Handles a user request to add a choosen keyword to PhD thesis
    """

    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    if request.method == "POST":
        user = auth.get_user(request)
        student = Student.objects.get(user = user)
        keyword = IEEEKeyword.objects.get(id = int(request.POST['id']))
        thesis = Thesis.objects.get(student = student)

        if thesis is not None:
            thesis_keyword = ThesisKeyword.objects.filter(thesis = thesis).filter(keyword = keyword)
            
            if thesis_keyword.count() == 0:
                thesis_keyword = ThesisKeyword(thesis = thesis, keyword = keyword)
                thesis_keyword.save()

                notification_message = 'Student ' + request.session['full_name'] + ' has added the keyword ' + keyword.keyword
                notification_message += ' for the PhD titled "' + thesis.title + '"'
                send_notification_to_guides(user, notification_message)
                # Email Notification
                subject = "[Keywords added] by " + request.session['full_name'];
                content = "<br>Dear Sir/Madam,</br><br></br><br></br>"+notification_message+'. Please Check the PhD Portal for more details.'+"<br></br><br></br>Regards,<br></br>PhDPortal."
                email = []

                for thesisGuide in ThesisGuide.objects.filter(thesis = thesis):
                    receiver = Faculty.objects.get(user = thesisGuide.guide.user)
                    email.append(receiver.email)

                send_email_task.delay(email, subject, content)
                return redirect(reverse(URL_STUDENT_ADD_KEYWORDS))
            else:
                # this keyword was already added
                return redirect(reverse(URL_BAD_REQUEST))
        else:
            return redirect(reverse(URL_FORBIDDEN))
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def student_phd_status(request):
    """
    View method. Renders a page where the student can see their PhD status.
    TODO: add status update logs to this view
    """

    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    if request.method == "GET":
        user = auth.get_user(request)
        student = Student.objects.get(user = user)
        thesis = Thesis.objects.get(student = student)
        phdStatus = thesis.status.id
        phdStatus_message = thesis.status.status_message
        phdStatuses = StatusType.objects.all().order_by('id')

        return render(
            request,
            'app/student/phd_status.html',
            {
                'title':'PhD Thesis Submission Status',
                'layout_data' : get_layout_data(request),
                'phdStatus' : phdStatus,
                'phdStatuses' : phdStatuses
            }
        )
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def student_help_procedure(request):
    """
    View method. Renders a help page consisting of procedure info.
    """

    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    if request.method == "GET":
        return render(
            request,
            'app/student/procedure.html',
            {
                'title':'Procedure',
                'layout_data' : get_layout_data(request),
            }
        )
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def student_help_contacts(request):
    """
    View method. Renders a view with hepl contacts.
    """

    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    if request.method == "GET":
        return render(
            request,
            'app/student/help_contacts.html',
            {
                'title':'Help Contacts',
                'layout_data' : get_layout_data(request),
            }
        )
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def student_cancel_synopsis(request):
    """
    Here the student can cancel the submission at an instant

    """
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))
    user = auth.get_user(request)
    student = Student.objects.get(user = user)
    thesis = Thesis.objects.get(student = student)

    if request.method == 'POST':
        _update_student_status(thesis, STATUS_ID_SUBMIT_SYNOPSIS)
        return redirect(reverse('student_upload_synopsis'))

    return redirect(reverse(URL_BAD_REQUEST))

@login_required
def student_cancel_thesis(request):

    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))
    user = auth.get_user(request)
    student = Student.objects.get(user = user)
    thesis = Thesis.objects.get(student = student)

    if request.method == 'POST':
        _update_student_status(thesis, STATUS_ID_SUBMIT_THESIS)
        return redirect(reverse('student_upload_thesis'))

    return redirect(reverse(URL_BAD_REQUEST))

@login_required
def student_keywords_print(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))
    user = auth.get_user(request)
    student = Student.objects.get(user = user)
    thesis = Thesis.objects.get(student = student)
    
    keywordList = []
    keys = ''
    
    i = 0
    for keyword in ThesisKeyword.objects.filter(thesis = thesis):
        i += 1

    j = 0
    for keyword in ThesisKeyword.objects.filter(thesis = thesis):
        keywordList.append(keyword.keyword)
        keys += str(keyword.keyword)
        j += 1
        if j == i:
            simply = 1
        else:
            keys += ', '

    for keyword in CustomKeyword.objects.filter(thesis = thesis):
        keys += ', '
        keywordList.append(keyword.keyword)
        keys += str(keyword.keyword)

    keys += '.'
    
    context = Context({
        'keywords' : keys
        })



    template = get_template('keywordtex.tex')
    
    rendered_tpl = template.render(context).encode('utf-8')  
    
    with tempfile.TemporaryDirectory() as tempdir:
        shutil.copy(os.getcwd()+"\\texput.tex",tempdir)
        
        with open(tempdir + '/texput.tex', 'wb') as file_:
            file_.write(rendered_tpl)
        
        for i in range(2):
            m = check_output('xelatex -interaction=nonstopmode -output-directory=' + tempdir + ' ' + tempdir + '\\texput.tex')
        
        with open(os.path.join(tempdir, 'texput.pdf'), 'rb') as f:
            pdf = f.read()

    r = HttpResponse(content_type = 'application/pdf')
    r['Content-Disposition'] = 'attachement;filename = keywords.pdf'
    r.write(pdf)
    return r

def _get_faculty_details(str):
    """
    Gets all the faculty'
    """
    faculties = Faculty.objects.filter(Q(first_name__icontains = str) | Q(last_name__icontains = str))
    result = []

    for faculty in faculties:
        if faculty.user.is_active == False:
            continue
        dict = {}
        dict['text'] = faculty.first_name + ' ' + faculty.last_name
        dict['email'] = faculty.email
        dict['id'] = faculty.id
        dict['username'] = faculty.user.username
        result.append(dict)

    return result

@login_required
def student_get_all_faculty_details(request):
    """
    Handles a user request for guide details
    This is accessed by a student
    Outputs JSON
    """

    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    if request.method == "GET":
        name = request.GET['term']
        return HttpResponse(json.dumps(_get_faculty_details(name)), content_type = 'application/json')
    else:
        return redirect(reverse(URL_BAD_REQUEST))