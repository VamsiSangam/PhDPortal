from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.template import RequestContext
from django.contrib import auth
from datetime import datetime
from app.models import *

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
                next = ''

                if next in request.GET:
                    next = request.GET['next']
                if next is None or next == '':
                    user = User.objects.get(username = username)
                    _add_user_data_to_session(user, request)

                    if (user.type == 'S'):                        
                        next = reverse('student_home')
                    elif (user.type == 'G'):
                        next = reverse('guide_home')
                    elif (user.type == 'D'):
                        next = reverse('director_home')
                    elif (user.type == 'R'):
                        next = reverse('referee_home')

                return redirect(next)
            else:
                return redirect('403/')
        else:
            return redirect('403/')

def logout(request):
    auth.logout(request)

    return redirect('/')