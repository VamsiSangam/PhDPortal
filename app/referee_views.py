from app.views import *

@login_required
def referee_home(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    return render(
        request,
        'app/referee/home.html',
        {
            'title':'Home Page',
            'descriptive_title' : 'Welcome Prof. Chong Chang!',
            'unread_notifications' : get_unread_notifications(request.session['username']),
        }
    )

@login_required
def referee_evaluate_synopsis(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))
    
    user = User.objects.get(username = request.session['username'])
    
    if request.method == "GET":
        all_thesis = []     # list of dict
        
        for panelMember in PanelMembers.objects.filter(referee_username = user).filter(status = 'N'):
            thesis = panelMember.thesis_id
            dict = {}
            dict['title'] = thesis.title
            dict['student_full_name'] = thesis.username.first_name + " " + thesis.username.last_name
            dict['synopsis'] = thesis.synopsis
            dict['student_username'] = thesis.username.username
            dict['id'] = thesis.id
            
            all_thesis.append(dict)
        
        return render(request, 'app/referee/evaluate_synopsis.html', {
            'title':'Unevaluated PhD Synopsis',
            'descriptive_title' : 'View unevaluated synopsis sumitted by PhD students',
            'unread_notifications' : get_unread_notifications(request.session['username']),
            'all_thesis' : all_thesis
        })
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def referee_synopsis_approval(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))
    
    referee = User.objects.get(username = request.session['username'])
    
    if request.method == "POST":
        id = int(request.POST['id'])
        isApproved = request.POST['isApproved'] == "True"
        feedback = request.POST['feedback']

        thesis = Thesis.objects.get(id = id)
        panelMember = PanelMembers.objects.filter(thesis_id = thesis).filter(referee_username = referee)[0]

        if isApproved:
            panelMember.status = 'A'
        else:
            panelMember.status = 'R'

        panelMember.save()

        dict = {'status' : 'OK', 'message' : 'Your response has been submitted successfully' }

        # notify guides & co-guides
        for thesisGuide in ThesisGuides.objects.filter(thesis_id = thesis):
            guide = thesisGuide.guide_username
            message = 'Referee ' + referee.first_name + ' ' + referee.last_name + ' '

            if isApproved:
                message += 'has approved to evaluate the PhD with title ' + thesis.title + '.'
            else:
                message += 'has rejected to evaluate the PhD with title ' + thesis.title + '.'

            if len(feedback.strip()) > 0:
                message += ' Referee has given the following feedback - ' + feedback

            send_notification(referee, guide, message, '')

        return HttpResponse(json.dumps(dict), content_type = 'application/json')
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def referee_evaluate_thesis(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    if request.method == "GET":
        return render(
            request,
            'app/referee/evaluate_thesis.html',
            {
                'title':'Evaluate Thesis',
                'descriptive_title' : 'Review PhD Thesis and give final feedbacks',
                'unread_notifications' : get_unread_notifications(request.session['username']),
            }
        )
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def referee_thesis_approval(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))
    
    referee = User.objects.get(username = request.session['username'])
    
    if request.method == "POST":
        
        dict = {'status' : 'OK', 'message' : 'Your response has been submitted successfully' }

        return HttpResponse(json.dumps(dict), content_type = 'application/json')
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def referee_evaluation_report(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    return render(
        request,
        'app/referee/submit_final_feedback.html',
        {
            'title':'Submit final evaluated report',
            'descriptive_title' : 'feedback submission button',
            'unread_notifications' : get_unread_notifications(request.session['username']),
        }
    )

@login_required
def referee_help_procedure(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    return render(
        request,
        'app/referee/procedure.html',
        {
            'title':'Procedure',
            'descriptive_title' : 'PhD Evaluation Procedure',
            'unread_notifications' : get_unread_notifications(request.session['username']),
        }
    )

@login_required
def referee_help_contacts(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    return render(
        request,
        'app/referee/help_contacts.html',
        {
            'title':'Help Contacts',
            'unread_notifications' : get_unread_notifications(request.session['username']),
        }
    )