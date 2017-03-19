from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.template import RequestContext
from django.contrib import auth
from datetime import datetime
from app.models import *
import json

def _get_unread_notifications(username):
    user = User.objects.get(username = username)
    unread_notifications = Notifications.objects.filter(receiver = user).filter(status = 'U')

    return unread_notifications

def student_home(request):
    assert isinstance(request, HttpRequest)
    
    unread_notifications = _get_unread_notifications(request.session['username'])

    return render(
        request,
        'app/student/home.html',
        {
            'title':'Home Page',
            'descriptive_title' : 'Welcome ' + request.session['first_name'] + ' !',
            'unread_notifications' : unread_notifications,
        }
    )

def student_edit_profile(request):
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/student/edit_profile.html',
        {
            'title':'Edit Profile',
            'descriptive_title' : 'Edit your profile',
        }
    )

def student_upload_synopsis(request):
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/student/upload_synopsis.html',
        {
            'title':'Upload Synopsis',
            'descriptive_title' : 'Upload Synopsis',
        }
    )

def student_view_synopsis(request):
    assert isinstance(request, HttpRequest)
    
    return render(
        request,
        'app/student/view_synopsis.html',
        {
            'title':'View Synopsis',
            'descriptive_title' : 'View you submitted synopsis',
        }
    )

def student_upload_thesis(request):
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/student/upload_thesis.html',
        {
            'title':'Upload Thesis',
            'descriptive_title' : 'Upload PhD Thesis',
        }
    )

def student_view_thesis(request):
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/student/view_thesis.html',
        {
            'title':'View Thesis',
            'descriptive_title' : 'View you submitted PhD thesis',
        }
    )

def student_add_keywords(request):
    assert isinstance(request, HttpRequest)

    user = User.objects.get(username = request.session['username'])
    
    # assumes that there will only be 1 phd thesis per user
    thesis = Thesis.objects.get(username = user)
    thesis_keywords = ThesisKeywords.objects.filter(thesis_id = thesis)

    return render(
        request,
        'app/student/add_keywords.html',
        {
            'title':'Add Keywords',
            'descriptive_title' : 'Add keywords to your PhD thesis',
            'thesis' : thesis,
            'thesis_keywords' : thesis_keywords,
        }
    )

def _validate_keyword(id, username):
    thesis_keyword = ThesisKeywords.objects.get(id = id)

    if thesis_keyword is not None:
        if thesis_keyword.thesis_id.username.username == username:
            return True

    return False

def student_delete_keyword(request, id):
    if request.method == "POST":
        if _validate_keyword(id, request.session['username']):
            thesis_keyword = ThesisKeywords.objects.get(id = id)
            thesis_keyword.delete()

            return redirect(reverse('student_add_keywords'))
    
    return redirect(reverse('unauthorized_access'))

def _ieee_keywords_to_list(keywords):
    list = []

    for keyword in keywords:
        dict = {}
        dict['id'] = keyword.id
        dict['keyword'] = keyword.keyword

        # count subkeywords
        dict['subkeywords'] = IEEEKeywords.objects.filter(parent_keyword_id = keyword).count()

        if keyword.parent_keyword_id is not None:
            dict['parent_id'] = keyword.parent_keyword_id.id

        list.append(dict)

    return list

def get_ieee_keywords(request):
    if request.method == "POST":
        parent_id = int(request.POST['parent_id'])
        keywords = None
        
        if parent_id == -1:
            keywords = IEEEKeywords.objects.filter(parent_keyword_id = None)
        else:
            parent_keyword = IEEEKeywords.objects.get(id = parent_id)

            if parent_keyword is not None:
                keywords = IEEEKeywords.objects.filter(parent_keyword_id = parent_keyword)
            else:
                return redirect(reverse('unauthorized_access'))
        
        result = _ieee_keywords_to_list(keywords)

        # add parent to result, if present
        if parent_id != -1:
            parent_keyword = IEEEKeywords.objects.get(id = parent_id)
            parent_keyword = parent_keyword.parent_keyword_id
            dict = {}

            if parent_keyword is not None:
                dict = {'id' : parent_keyword.id, 'keyword' : 'Go back to ' + parent_keyword.keyword }
            else:
                dict = {'id' : -1, 'keyword' : 'Go back '}

            result.append(dict)

        return HttpResponse(json.dumps(result), content_type = 'application/json')

def get_ieee_keywords_parent(request):
    if (request.method == "POST"):
        keyword = IEEEKeywords.objects.get(id = request.POST['parent_id'])
        id = keyword.parent_id.id

        if id is None:
            id = -1

        return HttpResponse(id, content_type = 'text/plain')
    
    return redirect(reverse('unauthorized_access'))

def student_add_keyword_to_thesis(request):
    if request.method == "POST":
        user = User.objects.get(username = request.session['username'])
        keyword = IEEEKeywords.objects.get(id = int(request.POST['id']))
        thesis = Thesis.objects.get(username = user)
        
        print('keyword - ' + keyword.keyword)
        print('thesis - ' + thesis.title)

        if thesis is not None:
            print('thesis is not none')
            thesis_keyword = ThesisKeywords.objects.filter(thesis_id = thesis).filter(keyword_id = keyword)
            #print('thesis_keyword - ' + thesis_keyword.count())

            if thesis_keyword.count() == 0:
                print('thesis_keyword is none')
                thesis_keyword = ThesisKeywords(thesis_id = thesis, keyword_id = keyword)
                thesis_keyword.save()

                return redirect(reverse('student_add_keywords'))

        return redirect(reverse('unauthorized_access'))

def student_phd_status(request):
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/student/phd_status.html',
        {
            'title':'PhD Thesis Submission Status',
            'descriptive_title' : 'PhD Thesis Submission Status',
        }
    )

def student_help_procedure(request):
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/student/procedure.html',
        {
            'title':'Procedure',
            'descriptive_title' : 'Having doubts about the submission procedure?',
        }
    )

def student_help_contacts(request):
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/student/help_contacts.html',
        {
            'title':'Help Contacts',
            'descriptive_title' : 'Contacts for critical issues',
        }
    )