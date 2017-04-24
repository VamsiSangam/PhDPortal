"""
Definition of views.
"""
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, render_to_response
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from app.models import *
from app.forms import *
import logging, json, operator
from datetime import datetime, time, timedelta
from tzlocal import get_localzone
import pytz
from django.core.mail import EmailMessage
from django.db.models import Q

logger = logging.getLogger('django')
CONTENT_TYPE_PDF = 'application/pdf'
MAX_SIZE_PDF = 5 * 1024 * 1024   # in bytes (currently 5 MB)
URL_BAD_REQUEST = 'bad_request'
URL_UNAUTHORIZED_ACCESS = 'unauthorized_access'
URL_FORBIDDEN = 'forbidden'
URL_NOT_FOUND = 'not_found'
URL_INTERNAL_SERVER_ERROR = 'internal_server_error'
URL_STUDENT_HOME = 'student_home'
URL_USER_PROFILE = 'user_profile'
STATUS_ID_THESIS_UNDER_EVALUATION = 21

def send_reminder_to_referees():
   # print("-*--*-*")
    for panelmember in PanelMember.objects.filter(status = 'S'):
        now = datetime.utcnow().replace(tzinfo=pytz.UTC)
    #    print(now)
        timediff = (now - panelmember.updated_time).days
     #   print(timediff)

        if int(timediff) >= 10:
            director = (Approver.objects.filter(active = True)[0]).faculty.user
            message = "This is a reminder to consider the invitaion and evaluate the synopsis of \"" + panelmember.thesis.title + "\". Please acknowledge us asap."
            send_notification(director, panelmember.referee.user, message, '')
      #      print(message)


def forgotpassword(request):
    """
    Forgot Pasword Module
    """
    if request.method == 'GET':
        return render(request, 'app/other/forgot_password.html', {'title':'Forgot Password?',})
    elif request.method == 'POST':

        username = request.POST['username']
        email = request.POST['email']
        if User.objects.filter(username = username).exists():
            default_password = 'HelloWorld'
            user = User.objects.get(username = username)
            if Referee.objects.filter(user = user).exists():
                referee = Referee.objects.get(user = user)
                user.set_password(default_password)
            else:
                dict = {message : ''}

        return redirect(reverse(URL_BAD_REQUEST))
    else:
        return redirect(reverse(URL_BAD_REQUEST))

def _get_user_type(user):
    """
    Returns a single character for a given username string denoting the user type

    Args:
        user: User model object

    Returns: 
        string object with single char - 'S', 'G', 'D', 'R'
    """

    type = None                
    print(user)
    if Student.objects.filter(user = user).exists():
        type = 'S'
    elif Faculty.objects.filter(user = user).exists():
        faculty = Faculty.objects.get(user = user)

        if Approver.objects.filter(faculty = faculty).exists():
            type = 'D'
        else:
            type = 'G'
    elif Referee.objects.filter(user = user).exists():
        type = 'R'
    elif Admin.objects.filter(user = user).exists():
        type = 'A'

    print(type)

    return type

def _get_user_type_object(user):
    """
    Returns the user type object based on which type the user is.
    Eg. for a student, method returns Student object.
    Pretty dangerous method to use

    Args:
        user : User model object
    """

    type = _get_user_type(user)

    if type == 'S':
        return Student.objects.get(user = user)
    elif type == 'G' or type == 'D':
        return Faculty.objects.get(user = user)
    elif type == 'R':
        return Referee.objects.get(user = user)
    elif type == 'A':
        return Admin.objects.get(user = user)

def _get_all_user_info(user):
    """
    Retrieves all user data for a given user

    Args:
        user: User model object

    Returns: 
        dict() object
    """

    dict = {}
    dict['username'] = user.get_username()
    dict['type'] = _get_user_type(user)

    if dict['type'] == 'S':
        _get_all_student_info(user, dict)
    elif dict['type'] == 'G' or dict['type'] == 'D':
        _get_all_guide_info(user, dict)
    elif dict['type'] == 'R':
        _get_all_referee_info(user, dict)
    elif dict['type'] == 'A':
        _get_all_admin_info(user, dict)
    return dict

def _get_all_referee_info(user, dict):
    """
    Adds referee info to dict, given a User object

    Args:
        user: User object
        dict: dict() object
    """
    dict['first_name'] = user.first_name
    dict['last_name'] = user.last_name
    dict['full_name'] = user.first_name + ' ' + user.last_name
    dict['email'] = user.email

def _get_all_admin_info(user, dict):
    """
    Adds referee info to dict, given a User object

    Args:
        user: User object
        dict: dict() object
    """
    dict['first_name'] = user.first_name
    dict['last_name'] = user.last_name
    dict['full_name'] = user.first_name + ' ' + user.last_name
    dict['email'] = user.email

def _get_all_student_info(user, dict):
    """
    Adds student info to dict, given a User object

    Args:
        user: User object
        dict: dict() object

    Returns: 
        None
    """

    student = Student.objects.get(user = user)

    dict['first_name'] = student.first_name
    dict['last_name'] = student.last_name
    dict['full_name'] = student.first_name + ' ' + student.last_name
    dict['email'] = student.email

    thesis = Thesis.objects.get(student = student)
    
    dict['title'] = thesis.title
    dict['thesis_id'] = thesis.id
    dict['abstract'] = thesis.abstract
    dict['guides'] = []
    dict['keywords'] = []
    
    thesisGuides = ThesisGuide.objects.filter(thesis = thesis)
    thesisKeywords = ThesisKeyword.objects.filter(thesis = thesis)

    for thesisGuide in thesisGuides:
        guide_info = {}

        if thesisGuide.type == 'G':
            guide_info['type'] = 'Guide'
        else:
            guide_info['type'] = 'Co-guide'

        guide = thesisGuide.guide
        guide_info['username'] = guide.user.username
        guide_info['full_name'] = guide.first_name + ' ' + guide.last_name
        dict['guides'].append(guide_info)

    for thesisKeyword in thesisKeywords:
        dict['keywords'].append(thesisKeyword.keyword.keyword)

    return dict

def _get_all_guide_info(user, dict):
    """
    Adds guide info to dict, given a User object

    Args:
        user: User object
        dict: dict() object

    Returns: 
        None
    """
    guide = Faculty.objects.get(user = user)
    
    dict['first_name'] = guide.first_name
    dict['last_name'] = guide.last_name
    dict['full_name'] = guide.first_name + ' ' + guide.last_name
    dict['email'] = guide.email
    
    thesisGuides = ThesisGuide.objects.filter(guide = guide)
    dict['all_thesis'] = []

    for thesisGuide in thesisGuides:
        thesis_info = {}

        if thesisGuide.type == 'G':
            thesis_info['type'] = 'Guide'
        else:
            thesis_info['type'] = 'Co-guide'

        thesis_info['title'] = thesisGuide.thesis.title
        student = thesisGuide.thesis.student
        thesis_info['student_username'] = student.user.username
        thesis_info['student_full_name'] = student.first_name + ' ' + student.last_name
        dict['all_thesis'].append(thesis_info)

    return dict

@login_required
def user_profile(request):
    """
    View method. Displays currently logged in user info
    """

    if request.method == "GET":
        user = _get_all_user_info(auth.get_user(request))

        return render(request, 'app/common/user_profile.html', {
            'title':'Home Page',
            'layout_data' : get_layout_data(request),
            'user' : user
        })
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def view_user_profile(request, username):
    """
    View method. Checks input 'username' and displays the 
    user info corresponding to the given 'username' parameter.
    """
    
    if request.method == "GET":
        user = User.objects.get(username = username)

        if user is None:    # checking if a user exists for the parameter
            return redirect(reverse(URL_BAD_REQUEST))

        user = _get_all_user_info(user)

        return render(request, 'app/common/user_profile.html', {
            'title': 'User - ' + user['full_name'],
            'layout_data' : get_layout_data(request),
            'user' : user
        })
    else:
        return redirect(reverse(URL_BAD_REQUEST))

def send_notification(sender, receiver, message, link):
    """
    Sends an unread notification to 'sender' from 'receiver' by adding a row to Notification model.

    Args:
        sender: User model object
        receiver: User model object
    """

    notification = Notification(sender = sender, receiver = receiver, message = message, link = link, status = 'U')
    notification.save()

def validate_request(request):
    """
    Validates a request. Eg. prevents student from accessing guide URLs etc.

    Returns:
        True : if the user has accessed a proper URL
        False : if the user has accessed a URL he/she shouldn't
    """

    if isinstance(request, HttpRequest):
        user = auth.get_user(request)
        type = _get_user_type(user)
        path = request.path

        if type == "S" and not (path.startswith('/user') or path.startswith('/student')):
            return False
        elif type == "G" and not (path.startswith('/user') or path.startswith('/guide')):
            return False
        elif type == "D" and not (path.startswith('/user') or path.startswith('/director')):
            return False
        elif type == "R" and not (path.startswith('/user') or path.startswith('/referee')):
            return False
        elif type == "A" and not (path.startswith('/user') or path.startswith('/admin')):
            return False
        return True
    else:
        return False
        
def validate_pdf(file_dict):
    """
    Validates a file submitted via POST form to be a valid PDF of valid size or not.

    Args:
        file_dict: request.FILES['file'] - dict object which has file details

    Returns:
        True : if file is a valid PDF
        False : if not
    """

    if file_dict.name.endswith('.pdf'):
        if file_dict.content_type == CONTENT_TYPE_PDF:
            if file_dict.size <= MAX_SIZE_PDF:
                return True

    return False

def _add_user_data_to_session(user, request):
    """
    Creates session variables 'username', 'type', 'first_name',
    'last_name', 'full_name', 'email' from given User model object

    Args:
        user: User model object
        request: request object
    """

    type = _get_user_type(user)
    request.session['username'] = user.get_username()
    request.session['type'] = type
    first_name = None
    last_name = None
    full_name  = None
    email = None

    if type == 'S':
        student = Student.objects.get(user = user)
        first_name = student.first_name
        last_name = student.last_name
        full_name = student.first_name + ' ' + student.last_name
        email = student.email
    elif type == 'G' or type == 'D':
        guide = Faculty.objects.get(user = user)
        first_name = guide.first_name
        last_name = guide.last_name
        full_name = guide.first_name + ' ' + guide.last_name
        email = guide.email
    elif type == 'R':
        first_name = user.first_name
        last_name = user.last_name
        full_name = user.first_name + ' ' + user.last_name
        email = user.email
    elif type == 'A':
        first_name = user.first_name
        last_name = user.last_name
        full_name = user.first_name + ' ' + user.last_name
        email = user.email
    request.session['first_name'] = first_name
    request.session['last_name'] = last_name
    request.session['full_name'] = full_name
    request.session['email'] = email

def login(request):
    """
    View method. Renders login page.
    """

    assert isinstance(request, HttpRequest)

    if request.method == 'GET':
        return render(request, 'app/other/login.html', {'title':'Login',})
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username, password = password)
        
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                logger.info('User %s successfully authenticated' % username)
                next = None

                if next in request.GET:
                    next = request.GET['next']
                else:
                    _add_user_data_to_session(auth.get_user(request), request)
                    next = reverse(URL_USER_PROFILE)

                return redirect(next)
            else:
                return redirect('403/')
        else:
            return redirect('403/')

@login_required
def logout(request):
    """
    Logout a user currently logged in by auth.login()
    """

    if request.method == "GET":
        logger.info('User %s successfully logged out' % request.session['username'])
        auth.logout(request)

        return redirect('/')
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def user_edit_profile(request):
    """
    View method. Renders user edit profile page.
    """

    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))
    
    if request.method == 'GET':
        user = auth.get_user(request)
        user_details = _get_user_type_object(user)

        return render(request, 'app/common/edit_profile.html', {
                'title':'Edit Profile',
                'layout_data' : get_layout_data(request),
                'user_details' : user_details
            })
    elif request.method == 'POST':
        user = auth.get_user(request)
        user = _get_user_type_object(user)  # temporary fix
        first_name = request.POST['first-name']
        last_name = request.POST['last-name']
        email_id = request.POST['email-id']
        address = request.POST['address']

        user.first_name = first_name
        user.last_name = last_name
        user.email = email_id
        user.save() 

        return redirect(reverse('user_edit_profile'))

    return redirect(reverse(URL_BAD_REQUEST))

#sending email
def send_text_email(receiver, subject, content):
    msg = EmailMessage(subject, content, to=[receiver])
    msg.content_subtype = "html"
    msg.send()

@login_required
def user_notifications(request):
    """
    View method. Displays notifications, read and unread of logged in user.
    """

    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    if request.method == "GET":
        user = auth.get_user(request)
        notifications = Notification.objects.filter(receiver = user).order_by('-date')
        read_notifications = notifications.filter(status = 'R')
        unread_notifications = notifications.filter(status = 'U')
        date = datetime.now(get_localzone())
        zone = date.tzinfo.zone

        return render(
            request,
            'app/common/notifications.html',
            {
                'title':'Notifications',
                'layout_data' : get_layout_data(request),
                'read_notifications': read_notifications,
                'unread_notifications': unread_notifications,
                'zone' : zone,  
            }
        )
    else:
        return redirect(reverse(URL_BAD_REQUEST))

def _verify_user_notification(user, id):
    """
    Verifies if the notification with the given id
    exists and the validates if the receiver is actually the user

    Args:
        user: User model object
        id: int, id in Notification model

    Returns:
        True : if notification exists and belongs to user
        False : invalid notification id / user
    """

    notification = Notification.objects.get(id = id)
    
    return (notification is not None) and (notification.receiver == user)

@login_required
def delete_user_notification(request, id):
    """
    Given notification id is validated if it belongs to
    logged in user. If valid, deletes it.

    Args:
        id: int, Notification model id
    """
    
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    if request.method == "POST" and _verify_user_notification(auth.get_user(request), id):
        notification = Notification.objects.get(id = id)
        notification.delete()

        return redirect(reverse('user_notifications'))
    else:
        return redirect(reverse('unauthorized_access'))

@login_required
def delete_all_unread_notifications(request):
    """
    Handles a request to delete all unread notifications of a user.
    """

    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))
    
    if request.method == "POST":
        user = auth.get_user(request)
        notifications = Notification.objects.filter(receiver = user).filter(status = 'U')
        notifications.delete()

        return redirect(reverse('user_notifications'))
    else:
        return redirect(reverse('unauthorized_access'))

@login_required
def delete_all_read_notifications(request):
    """
    Handles a request to delete all read notifications.
    """

    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    if request.method == "POST":
        user = auth.get_user(request)
        notifications = Notification.objects.filter(receiver = user).filter(status = 'R')
        notifications.delete()

        return redirect(reverse('user_notifications'))
    else:
        return redirect(reverse('unauthorized_access'))

@login_required
def mark_all_notifications_read(request):
    """
    Handles a user request to mark all unread notifications as read
    """

    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    if request.method == "POST":
        user = auth.get_user(request)
        notifications = Notification.objects.filter(receiver = user).filter(status = 'U')

        for notification in notifications:
            notification.status = 'R'
            notification.save()

        return redirect(reverse('user_notifications'))
    else:
        return redirect(reverse('unauthorized_access'))

@login_required
def mark_notification_read(request, id):
    """
    Handles a user request to mark an unread notification as read.
    Validates the notification id and makes changes.
    """
    
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    if request.method == "POST" and _verify_user_notification(auth.get_user(request), id):
        notification = Notification.objects.get(id = id)
        notification.status = 'R'
        notification.save()

        return redirect(reverse('user_notifications'))
    else:
        return redirect(reverse('unauthorized_access'))

@login_required
def search_user(request):
    """
    View method. Renders a search utility to search for users.
    """

    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))
    if request.session['type'] == 'S' or request.session['type'] == 'R': return redirect(reverse(URL_FORBIDDEN))

    if request.method == "GET":
        return render(
            request,
            'app/common/search_user.html',
            {
                'title':'Student Info',
                'layout_data' : get_layout_data(request),
            }
        )
    else:
        return redirect(reverse(URL_BAD_REQUEST))

def _clean_user_info_results(data):
    """
    Converts data to a JSON convertable object

    Args:
        data : Sorted list of tuples

    Returns:
        list of dictionaries, where each dict has keys -
        'username', 'first_name', 'last_name', 'email', 'type'
    """

    list = []

    for user in data[: min(len(data), 15)]:
        dict = _get_all_user_info(user[0])
        list.append(dict)

    return list

@login_required
def search_user_query(request):
    """
    Handles an AJAX request from the search user view

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
            print('Queried User type = ' + user_type)
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

        # print sorted results
        for item in sorted_results:
            print(item)
        print('\n')

        result = _clean_user_info_results(sorted_results)

        return HttpResponse(json.dumps(result), content_type = 'application/json')
    else:
        return redirect(reverse(URL_BAD_REQUEST))

def get_referee_recommendations(thesis):
    """
    Returns referee recommendations for a given thesis id

    Args:
        thesis: Thesis model object

    Returns: 
        dictionary of indian and foreign referee information
    """

    dict = {}
    keywords = []   # a list of thesis keyword ids
    referees = []   # a list of current thesis' referee model ID
    MAX_RECOMMENDATIONS = 10
    
    # query thesis keyword ids
    for thesis_keyword in ThesisKeyword.objects.filter(thesis = thesis):
        keywords.append(thesis_keyword.keyword.id)

    print('Thesis - ' + thesis.title + " has " + str(len(keywords)) + " keywords")

    # query current thesis referees, store referee model ID
    for panel_member in PanelMember.objects.filter(thesis = thesis):
        referees.append(panel_member.referee.id)

    print('Thesis - ' + thesis.title + " has " + str(len(referees)) + " referees")

    # query all archived thesis => whose status >= STATUS_ID_THESIS_UNDER_EVALUATION
    for archived_thesis in Thesis.objects.filter(status__id__gte = STATUS_ID_THESIS_UNDER_EVALUATION):
        similarity = 0

        # count how many keywords match
        for thesis_keyword in ThesisKeyword.objects.filter(thesis = archived_thesis):
            if thesis_keyword.keyword.id in keywords:
                similarity += 1
        
        # query for all approved status = Approved/FeedbackSubmitted/FeedbackSubmitted & need Re-Evaluation
        for panel_member in PanelMember.objects.filter(thesis = archived_thesis) \
            .filter(Q(status = 'A') | Q(status = 'F') | Q(status = 'Z')):
            referee = panel_member.referee

            if not (referee.id in referees):
                if referee in dict:
                    dict[referee] += similarity
                else:
                    dict[referee] = similarity

    print('Thesis - ' + thesis.title + " has found " + str(len(dict)) + " matches")
    
    # filter results
    sorted_results = sorted(dict.items(), key = operator.itemgetter(1))
    sorted_results.reverse()

    indian = []
    foreign = []
    
    for tuple in sorted_results:
        referee = tuple[0]
        details = {}           
        details['username'] = referee.user.username
        details['full_name'] = referee.user.first_name + " " + referee.user.last_name
        details['address'] = "No yet included in database"  # Need to change
        details['designation'] = referee.designation
        details['website'] = referee.website
        details['university'] = referee.university

        if referee.type == "I" and len(indian) < MAX_RECOMMENDATIONS:
            details['type'] = "Indian"
            indian.append(details)
        elif len(foreign) < MAX_RECOMMENDATIONS:
            details['type'] = "Foreign"
            foreign.append(details)
        else:
            break

    print('Thesis - ' + thesis.title + " has " + str(len(indian)) + " indian referee recommendations")
    print('Thesis - ' + thesis.title + " has " + str(len(foreign)) + " foreign referee recommendations")
    
    return {'indian' : indian, 'foreign': foreign}

def get_layout_data(request):
    """
    Returns a dict with keys 'unread_notifications_count' and 
    'unread_notifications' which are used for display purposes

    Args:
        param1: This is the first param.

    Returns:
        dict object
    """
    
    user = auth.get_user(request)
    dict = {}
    dict['unread_notifications_count'] = Notification.objects.filter(receiver = user).filter(status = 'U').count()
    dict['unread_notifications'] = Notification.objects.filter(receiver = user).filter(status = 'U')[:3]
    #dict['unread_notifications_count'] = 0
    #dict['unread_notifications'] = None

    return dict

def bad_request(request):
    """
    View method for displaying a 400 status message.
    Returns a view with a 400 HTTP status code.
    """
    
    assert isinstance(request, HttpRequest)

    response = render_to_response(
        'app/layouts/error.html',
        {
            'title':'Bad Request',
            'status_code' : 400,
            'message' : 'The request cannot be fulfilled due to conflicting data/validation or was leading to invalid state.',
        }
    )

    response.status_code = 400

    return response

def not_found(request):
    """
    View method for displaying a 404 status message.
    Returns a view with a 404 HTTP status code.
    """

    assert isinstance(request, HttpRequest)

    response = render_to_response(
        'app/layouts/error.html',
        {
            'title':'Not found',
            'status_code' : 404,
            'message' : 'The resource you accessed doesn\'t exist or may have been moved to a new location',
        }
    )

    response.status_code = 404

    return response

def unauthorized_access(request):
    """
    View method for displaying a 401 status message.
    Returns a view with a 401 HTTP status code.
    """

    assert isinstance(request, HttpRequest)

    response = render_to_response(
        'app/layouts/error.html',
        {
            'title':'Unauthorised Access',
            'status_code' : 401,
            'message' : 'You need to log in with proper credentials to access this resource.',
        }
    )

    response.status_code = 401

    return response

def forbidden(request):
    """
    View method for displaying a 403 status message.
    Returns a view with a 403 HTTP status code.
    """

    assert isinstance(request, HttpRequest)

    response = render_to_response(
        'app/layouts/error.html',
        {
            'title':'Forbidden',
            'status_code' : 403,
            'message' : 'You are not allowed to access this resource.',
        }
    )

    response.status_code = 403

    return response

def internal_server_error(request):
    """
    View method for displaying a 500 status message.
    Returns a view with a 500 HTTP status code.
    """

    assert isinstance(request, HttpRequest)

    response = render_to_response(
        'app/layouts/error.html',
        {
            'title':'Internal Server Error',
            'status_code' : 500,
            'message' : 'The server encountered a problem. The issue has been logged. Please try again later.',
        }
    )

    response.status_code = 500

    return response