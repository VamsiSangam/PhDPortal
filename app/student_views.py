from app.views import *
import datetime
from datetime import time, timedelta
from django.utils.datastructures import MultiValueDictKeyError
from app.tasks import send_email_task

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

        return render(request, 'app/student/phd_add_details.html', {
            'layout_data' : get_layout_data(request),
            'isDetailsApproved' : isDetailsApproved
        })
    elif request.method == "POST" and (not isDetailsApproved):
        title = request.POST['title']
        guide_1 = request.POST['guide-1']
        guide_2 = request.POST['guide-2']
        co_guide = request.POST['co_guide']
        print(title)
        if (guide_1 == 'None' and guide_2 == 'None' and co_guide == 'None') or (guide_1 != 'None' and guide_2 != 'None' and co_guide != 'None') or (guide_1 == 'None' and guide_2 == 'None'):
            #dict = {'status' : 'OK', 'message' : 'Please Update The Details Properly According to the rules!'}
            print('herererererere')
            return render(request, 'app/student/phd_add_details.html', {
            'layout_data' : get_layout_data(request),
            'isDetailsApproved' : isDetailsApproved,
            'detailsError' : True,
            'detailsErrorMessage' : 'Please Update The Details Properly According to the rules!'
        })
        else :

            thesis.title = title
            thesis.save()
            
            if guide_1 != 'None':
                guide_1 = int(guide_1)
                guide = Faculty.objects.get(id = guide_1)
                ThesisGuide(thesis = thesis, guide = guide, type = 'G').save()
            
            if guide_2 != 'None':
                guide_2 = int(guide_2)
                guide = Faculty.objects.get(id = guide_2)
                ThesisGuide(thesis = thesis, guide = guide, type = 'G').save()
            
            if co_guide != 'None':
                co_guide = int(co_guide)
                guide = Faculty.objects.get(id = co_guide)
                ThesisGuide(thesis = thesis, guide = guide, type = 'C').save()
            
            _update_student_status(thesis, STATUS_ID_SUBMIT_ABSTRACT) 
            #notification_message = 'Student ' + request.session['full_name'] + ' has submitted their PhD abstract '
            #notification_message += 'for the PhD titled "' + thesis.title + '"'
            #send_notification_to_guides(user, notification_message)
            #_update_student_status(thesis, STATUS_ID_ABSTRACT_APPROVED - 1)

            return redirect(reverse(URL_STUDENT_ADD_DETAILS))

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
        ##sending email
        ##Email Notification
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
        
       # return redirect(reverse(URL_STUDENT_ADD_ABSTRACT))
        return redirect(reverse(URL_STUDENT_ADD_ABSTRACT)) 
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def student_request_synopsis(request):
    """
    View method. Renders a page where student can submit PhD synopsis
    """
    
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))
    
    user = auth.get_user(request)
    student = Student.objects.get(user = user)
    thesis = Thesis.objects.get(student = student)
   
    
    if request.method == 'POST':
        _update_student_status(thesis, STATUS_ID_REQUEST_PENDING_BY_SPGC_TO_UPLOAD_SYNOPSIS)
        ##notify admin to give permission to upload synopsis
        admin = Admin.objects.all()[0]
        notify = "Respected Sir/Madam! Please grant me the permission to upload the synopsis on portal, since I completed my credits."
        send_notification(user, admin.user, notify, '')
        #send email --fill this afterwards
        #email to referee
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
                 ##Email Notification
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
            thesis.save()

            notification_message = 'Student ' + request.session['full_name'] + ' has submitted their PhD thesis document '
            notification_message += 'for the PhD titled "' + thesis.title + '"'
            send_notification_to_guides(user, notification_message)
            ##Email Notification
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
        
        if form.is_valid() and validate_pdf(request.FILES['thesis']):    
            thesis.thesis = request.FILES['thesis']
            thesis.save()

            notification_message = 'Student ' + request.session['full_name'] + ' has Re-submitted their PhD thesis document after modifications'
            notification_message += 'for the PhD titled "' + thesis.title + '"'
            send_notification_to_guides(user, notification_message)
            ##Email Notification
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
            }
        )
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def student_search_keywords(request):
    """
    Handles an AJAX request for keyword search
    """

    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    if request.method == "POST":
        keyword_typed = request.POST['keyword-typed']
        keywords = IEEEKeyword.objects.filter(keyword__icontains = keyword_typed)

        # TODO : add logic to send atmost 20 search results
        # TODO : add logic to remove keywords already added to thesis

        result = _ieee_keywords_to_list(keywords)

        return HttpResponse(json.dumps(result), content_type = 'application/json')
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def student_keyword_recommendations(request):
    """
    Handles AJAX request to load a student's recommended keywords
    """
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    if request.method == "POST":
        keywords = IEEEKeyword.objects.filter(keyword__icontains = 'process')

        # TODO : add recommender logic here, output format should be same
        #        as that of what is returned from _ieee_keywords_to_list.
        #        A list of dict with keys - id, keyword
        #        Keys parent, subkeywords not needed.
        #        Recommendations should never be 0. Have an upper limit.

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
        parent = int(request.POST['parent'])

        # TODO : implement adding custom keyword logic here. If u want to send an error message
        #        follow the format below. If keyword is added successfully then redirect to
        #        add keywords page.

        result = {'message' : 'error message'}

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

        # add parent to result, if present - this is used to create go back link
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
                ##Email Notification
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
        print(phdStatus_message)
        
        print(phdStatus)
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