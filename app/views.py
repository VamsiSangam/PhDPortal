"""
Definition of views.
"""
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, render_to_response
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from app.models import *
import logging, json, operator

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

def _get_all_user_info(user):
    dict = {}
    dict['username'] = user.username
    dict['first_name'] = user.first_name
    dict['last_name'] = user.last_name
    dict['full_name'] = user.first_name + ' ' + user.last_name
    dict['email_id'] = user.email_id
    dict['address'] = user.address
    dict['type'] = user.type

    if user.type == 'S':
        _get_all_student_info(user, dict)
    elif user.type == 'G':
        _get_all_guide_info(user, dict)

    return dict

def _get_all_student_info(user, dict):
    thesis = Thesis.objects.get(username = user)
    dict['title'] = thesis.title
    dict['abstract'] = thesis.abstract
    dict['guides'] = []
    dict['keywords'] = []
    thesisGuides = ThesisGuides.objects.filter(thesis_id = thesis)
    thesisKeywords = ThesisKeywords.objects.filter(thesis_id = thesis)

    for thesisGuide in thesisGuides:
        guide_info = {}

        if thesisGuide.type == 'G':
            guide_info['type'] = 'Guide'
        else:
            guide_info['type'] = 'Co-guide'

        thesisGuide = thesisGuide.guide_username
        guide_info['username'] = thesisGuide.username
        guide_info['full_name'] = thesisGuide.first_name + ' ' + thesisGuide.last_name
        dict['guides'].append(guide_info)

    for thesisKeyword in thesisKeywords:
        dict['keywords'].append(thesisKeyword.keyword_id.keyword)

    return dict

def _get_all_guide_info(user, dict):
    all_thesis = ThesisGuides.objects.filter(guide_username = user)
    dict['all_thesis'] = []

    for thesis in all_thesis:
        thesis_info = {}

        if thesis.type == 'G':
            thesis_info['type'] = 'Guide'
        else:
            thesis_info['type'] = 'Co-guide'

        thesis_info['title'] = thesis.thesis_id.title
        student = thesis.thesis_id.username
        thesis_info['student_username'] = student.username
        thesis_info['student_full_name'] = student.first_name + ' ' + student.last_name
        dict['all_thesis'].append(thesis_info)

    return dict

@login_required
def user_profile(request):
    if request.method == "GET":
        user = User.objects.get(username = request.session['username'])
        user = _get_all_user_info(user)

        return render(request, 'app/common/user_profile.html', {
            'title':'Home Page',
            'descriptive_title' : 'Welcome ' + request.session['full_name'] + ' !',
            'unread_notifications' : get_unread_notifications(request.session['username']),
            'user' : user
        })
    else:
        return redirect(reverse(URL_BAD_REQUEST))

def view_user_profile(request, username):
    if request.method == "GET":
        user = User.objects.get(username = username)

        if user is None:
            return redirect(reverse(URL_BAD_REQUEST))

        user = _get_all_user_info(user)

        return render(request, 'app/common/user_profile.html', {
            'title':'Home Page',
            'descriptive_title' : 'User ' + username + ' info',
            'unread_notifications' : get_unread_notifications(request.session['username']),
            'user' : user
        })
    else:
        return redirect(reverse(URL_BAD_REQUEST))

def send_notification(sender, receiver, message, link):
    notification = Notifications(sender = sender, receiver = receiver, message = message, link = link, status = 'U')
    notification.save()

def validate_request(request):
    if isinstance(request, HttpRequest):
        user = User.objects.get(username = request.session['username'])
        type = user.type
        path = request.path

        if type == "S" and not (path.startswith('/user') or path.startswith('/student')):
            return False
        elif type == "G" and not (path.startswith('/user') or path.startswith('/guide')):
            return False
        elif type == "D" and not (path.startswith('/user') or path.startswith('/director')):
            return False
        elif type == "R" and not (path.startswith('/user') or path.startswith('/referee')):
            return False
        return True
    else:
        return False
        
def validate_pdf(file_dict):
    if file_dict.name.endswith('.pdf'):
        if file_dict.content_type == CONTENT_TYPE_PDF:
            if file_dict.size <= MAX_SIZE_PDF:
                return True

    return False

def get_unread_notifications(username):
    user = User.objects.get(username = username)
    unread_notifications = Notifications.objects.filter(receiver = user).filter(status = 'U')

    return unread_notifications

def _add_user_data_to_session(user, request):
    request.session['username'] = user.username
    request.session['first_name'] = user.first_name
    request.session['last_name'] = user.last_name
    request.session['full_name'] = user.first_name + ' ' + user.last_name
    request.session['email_id'] = user.email_id
    request.session['type'] = user.type

def login(request):
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
                next = ''

                if next in request.GET:
                    next = request.GET['next']
                if next is None or next == '':
                    user = User.objects.get(username = username)
                    _add_user_data_to_session(user, request)
                    
                    next = reverse(URL_USER_PROFILE)
                return redirect(next)
            else:
                return redirect('403/')
        else:
            return redirect('403/')

@login_required
def logout(request):
    logger.info('User %s successfully logged out' % request.session['username'])
    auth.logout(request)

    return redirect('/')

def _get_notifications_for_user(username):
    notifications = Notifications.objects.filter(receiver = username)

    return notifications

@login_required
def user_edit_profile(request):
    validate_request(request)
    
    if request.method == 'GET':
        user_details = User.objects.get(username = request.session['username'])

        return render(request, 'app/common/edit_profile.html', {
                'title':'Notifications',
                'descriptive_title' : 'All notifications',
                'unread_notifications' : get_unread_notifications(request.session['username']),
                'user_details' : user_details
            })
    elif request.method == 'POST':
        user_name = request.session['username']
        user_details = User.objects.get(username = user_name)
        first_name = request.POST['first-name']
        last_name = request.POST['last-name']
        email_id = request.POST['email-id']
        address = request.POST['address']

        user_details.first_name = first_name
        user_details.last_name = last_name
        user_details.email_id = email_id
        user_details.address = address
        user_details.save() 

        return redirect(reverse('user_edit_profile'))

    return redirect(reverse('unauthorized_access'))

@login_required
def user_notifications(request):
    validate_request(request)

    notifications = _get_notifications_for_user(request.session['username'])
    read_notifications = notifications.filter(status = 'R')
    unread_notifications = notifications.filter(status = 'U')

    return render(
        request,
        'app/common/notifications.html',
        {
            'title':'Notifications',
            'descriptive_title' : 'All notifications',
            'read_notifications': read_notifications,
            'unread_notifications': unread_notifications,
        }
    )

def _verify_user_notification(username, id):
    notification = Notifications.objects.get(id = id)
    
    return (notification is not None) and (notification.receiver.username == username)

@login_required
def delete_user_notification(request, id):
    validate_request(request)

    if request.method == "POST" and _verify_user_notification(request.session['username'], id):
        notification = Notifications.objects.get(id = id)
        notification.delete()

        return redirect(reverse('user_notifications'))
    else:
        return redirect(reverse('unauthorized_access'))

@login_required
def delete_all_unread_notifications(request):
    validate_request(request)
    
    if request.method == "POST":
        user = User.objects.get(username = request.session['username'])
        notifications = Notifications.objects.filter(receiver = user).filter(status = 'U')
        notifications.delete()

        return redirect(reverse('user_notifications'))
    else:
        return redirect(reverse('unauthorized_access'))

@login_required
def delete_all_read_notifications(request):
    validate_request(request)

    if request.method == "POST":
        user = User.objects.get(username = request.session['username'])
        notifications = Notifications.objects.filter(receiver = user).filter(status = 'R')
        notifications.delete()

        return redirect(reverse('user_notifications'))
    else:
        return redirect(reverse('unauthorized_access'))

@login_required
def mark_all_notifications_read(request):
    validate_request(request)

    if request.method == "POST":
        user = User.objects.get(username = request.session['username'])
        notifications = Notifications.objects.filter(receiver = user).filter(status = 'U')

        for notification in notifications:
            notification.status = 'R'
            notification.save()

        return redirect(reverse('user_notifications'))
    else:
        return redirect(reverse('unauthorized_access'))

@login_required
def mark_notification_read(request, id):
    validate_request(request)

    if request.method == "POST" and _verify_user_notification(request.session['username'], id):
        notification = Notifications.objects.get(id = id)
        notification.status = 'R'
        notification.save()

        return redirect(reverse('user_notifications'))
    else:
        return redirect(reverse('unauthorized_access'))

@login_required
def search_user(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    
    if request.method == "GET":
        return render(
            request,
            'app/common/search_user.html',
            {
                'title':'Student Info',
                'descriptive_title' : 'View information about PhD students',
                'unread_notifications' : get_unread_notifications(request.session['username'])
            }
        )
    else:
        return redirect(reverse(URL_BAD_REQUEST))

def _clean_user_info_results(data):
    # data is sorted list of tuple
    list = []

    for item in data[: min(len(data), 15)]:
        dict = {}
        dict['username'] = item[0].username
        dict['first_name'] = item[0].first_name
        dict['last_name'] = item[0].last_name
        dict['email_id'] = item[0].email_id
        dict['type'] = item[0].type
        dict['address'] = item[0].address
        list.append(dict)

    return list

@login_required
def search_user_query(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        type = request.POST['type']

        dict = {}
        for user in User.objects.filter(type = type):
            dict[user] = 3
            
        if len(first_name.strip()) > 0:
            for user in User.objects.filter(first_name__icontains = first_name):
                if user in dict:
                    dict[user] = dict[user] + 1
                else:
                    dict[user] = 1

        if len(last_name.strip()) > 0:
            for user in User.objects.filter(last_name__icontains = last_name):
                if user in dict:
                    dict[user] = dict[user] + 1
                else:
                    dict[user] = 1
        
        if len(email.strip()) > 0:
            for user in User.objects.filter(email_id__icontains = email):
                if user in dict:
                    dict[user] = dict[user] + 1
                else:
                    dict[user] = 1

        sorted_results = sorted(dict.items(), key = operator.itemgetter(1))
        sorted_results.reverse()
        result = _clean_user_info_results(sorted_results)

        return HttpResponse(json.dumps(result), content_type = 'application/json')
    else:
        return redirect(reverse(URL_BAD_REQUEST))

def bad_request(request):
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