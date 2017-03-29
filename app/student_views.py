from app.views import *

URL_STUDENT_ADD_ABSTRACT = 'student_add_abstract'
URL_STUDENT_VIEW_THESIS = 'student_view_thesis'
URL_STUDENT_ADD_KEYWORDS = 'student_add_keywords'
STATUS_ID_SUBMIT_ABSTRACT = 5
STATUS_ID_ABSTRACT_APPROVED = 7
STATUS_ID_SUBMIT_SYNOPSIS = 9
STATUS_ID_SYNOPSIS_APPROVED = 11
STATUS_ID_SUBMIT_THESIS = 13
STATUS_ID_THESIS_APPROVED = 15
STATUS_ID_PANEL_SENT = 17
STATUS_ID_PANEL_APPROVED = 19
STATUS_ID_THESIS_UNDER_EVALUATION = 21

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
def student_add_abstract(request):
    """
    View method. Renders a page where student can submit PhD abstract
    """
    
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))
    
    user = auth.get_user(request)
    student = Student.objects.get(user = user)
    thesis = Thesis.objects.get(student = student)
    canSubmitAbstract = thesis.status.id >= STATUS_ID_SUBMIT_ABSTRACT
    isAbstractApproved = thesis.status.id >= STATUS_ID_ABSTRACT_APPROVED

    if request.method == "GET":
        abstract = thesis.abstract

        return render(request, 'app/student/phd_abstract.html', {
            'title' : 'PhD Abstract',
            'layout_data' : get_layout_data(request),
            'abstract' : abstract,
            'canSubmitAbstract' : canSubmitAbstract,
            'isAbstractApproved' : isAbstractApproved
        })
    elif request.method == "POST" and canSubmitAbstract and (not isAbstractApproved):
        abstract = request.POST['abstract']
        thesis.abstract = abstract
        thesis.save()

        notification_message = 'Student ' + request.session['full_name'] + ' has submitted their PhD abstract '
        notification_message += 'for the PhD titled "' + thesis.title + '"'
        send_notification_to_guides(user, notification_message)
        _update_student_status(thesis, STATUS_ID_ABSTRACT_APPROVED - 1)
        
        return redirect(reverse(URL_STUDENT_ADD_ABSTRACT))
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
    canSubmitSynopsis = thesis.status.id >= STATUS_ID_SUBMIT_SYNOPSIS
    isSynopsisApproved = thesis.status.id >= STATUS_ID_SYNOPSIS_APPROVED

    if request.method == 'GET':
        return render(
            request,
            'app/student/upload_synopsis.html',
            {   
                'title' : 'Upload Synopsis',
                'layout_data' : get_layout_data(request),
                'canSubmitSynopsis' : canSubmitSynopsis,
                'isSynopsisApproved' : isSynopsisApproved
            }
        )
    elif request.method == "POST" and canSubmitSynopsis and (not isSynopsisApproved):
        form = SynopsisForm(request.POST, request.FILES)
        
        if form.is_valid() and validate_pdf(request.FILES['synopsis']):
            thesis.synopsis = request.FILES['synopsis']
            thesis.save()

            notification_message = 'Student ' + request.session['full_name'] + ' has submitted their PhD synopsis '
            notification_message += 'for the PhD titled "' + thesis.title + '"'
            send_notification_to_guides(user, notification_message)
            _update_student_status(thesis, STATUS_ID_SYNOPSIS_APPROVED - 1)

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
    isThesisApproved = thesis.status.id >= STATUS_ID_THESIS_APPROVED

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
                'isThesisApproved' : isThesisApproved
            }
        )
    elif request.method == "POST" and canSubmitThesis and (not isThesisApproved):
        form = ThesisForm(request.POST, request.FILES)
        
        if form.is_valid() and validate_pdf(request.FILES['thesis']):    
            thesis.thesis = request.FILES['thesis']
            thesis.save()

            notification_message = 'Student ' + request.session['full_name'] + ' has submitted their PhD thesis document '
            notification_message += 'for the PhD titled "' + thesis.title + '"'
            send_notification_to_guides(user, notification_message)
            _update_student_status(thesis, STATUS_ID_THESIS_APPROVED - 1)

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
                'thesis_keywords' : thesis_keywords,
            }
        )
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
        phdStatuses = StatusType.objects.all()

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