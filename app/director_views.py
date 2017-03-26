from app.views import *
from app.student_views import *

@login_required
def director_home(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    return render(
        request,
        'app/director/home.html',
        {
            'title':'Home Page',
            'descriptive_title' : 'Welcome ' + request.session['full_name'] + ' !',
            'unread_notifications' : get_unread_notifications(request.session['username'])
        }
    )

@login_required
def director_edit_profile(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    return render(
        request,
        'app/director/edit_profile.html',
        {
            'title':'Edit Profile',
            'descriptive_title' : 'Edit your profile',
            'unread_notifications' : get_unread_notifications(request.session['username'])
        }
    )

@login_required
def director_view_student_info(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    if request.method == "GET":
        all_thesis = []     # list of dict
        for thesis_object in Thesis.objects.all():
            dict = {}
            dict['title'] = thesis_object.title
            dict['student_full_name'] = thesis_object.username.first_name+" "+thesis_object.username.last_name
            dict['student_username'] = thesis_object.username.username
            dict['id'] = thesis_object.id
            dict['status_message'] = thesis_object.status.status_message
            all_thesis.append(dict)
        return render(
            request,
            'app/director/view_student_info.html',
            {
                'title':'PhD Status',
                'descriptive_title' : 'View the status of ongoing PhDs',
                'unread_notifications' : get_unread_notifications(request.session['username']),
                'all_thesis' : all_thesis
            }
        )
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def director_submit_for_evaluation(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))
    
    if request.method == "GET": # post only for testing
        all_list = []     # list of dict
        for thesis in Thesis.objects.all():
            this_thesis = {}
            logger.info(thesis.title + " ------- ==== >]")

            #need to use one more status if referees are out of bound
            if thesis.status.id >= STATUS_ID_PANEL_APPROVED and thesis.status.id < STATUS_ID_THESIS_UNDER_EVALUATION:
                logger.info(thesis.title + " ------- ==== > PASS]")
                #storing thesis information
                this_thesis['id'] = thesis.id
                this_thesis['username'] = thesis.username.username
                this_thesis['fullname'] = thesis.username.first_name + " " + thesis.username.last_name
                this_thesis['title'] = thesis.title
                this_thesis['abstract'] = thesis.abstract
                this_thesis['guides'] = []
                #storing guides of a thesis
                for thesis_guides in ThesisGuides.objects.filter(thesis_id = thesis):
                    dict = {}
                    dict['username'] = thesis_guides.guide_username.username
                    dict['fullname'] = thesis_guides.guide_username.first_name + " " + thesis_guides.guide_username.last_name
                    if thesis_guides.type == 'G':
                        dict['type'] = 'Guide'
                    else:
                        dict['type'] = 'Co-Guide'
                    this_thesis['guides'].append(dict)
                #storing referee information
                this_thesis['indian_referees'] = []
                this_thesis['foreign_referees'] = []
                this_thesis['total_indian_panel'] = 0
                this_thesis['total_foreign_panel'] = 0
                for panel in PanelMembers.objects.filter(thesis_id = thesis).filter(status = 'A'): #if the panel is approved(A) only
                    dict = {}
                    dict['username'] = panel.referee_username.username
                    dict['fullname'] = panel.referee_username.first_name + " " + panel.referee_username.last_name
                    dict['address'] = panel.referee_username.address
                    referee = Referees.objects.get(user = panel.referee_username)
                    if referee.type == 'I':
                        dict['type'] = 'Indian'
                        this_thesis['indian_referees'].append(dict)
                    else:
                        dict['type'] = 'Foreign'
                        this_thesis['foreign_referees'].append(dict)
                #storing thesis keywords
                this_thesis['keywords'] = []
                for keys in ThesisKeywords.objects.filter(thesis_id = thesis):
                    this_thesis['keywords'].append((IEEEKeywords.objects.get(id = keys.keyword_id.id)).keyword)
                this_thesis['required_indian'] = INDIAN_REFEREES
                this_thesis['required_foreign'] = FOREIGN_REFEREES
                for finalpanel in FinalPanel.objects.filter(thesis_id = thesis):
                    referee = Referees.objects.get(user = finalpanel.referee_username)
                    if referee.type == 'I' and finalpanel.status == 'Approved':
                        this_thesis['required_indian'] -= 1
                    if referee.type == 'F' and finalpanel.status == 'Approved':
                        this_thesis['required_foreign'] -= 1
                all_list.append(this_thesis)
             
        return render(
            request,
            'app/director/submit_for_evaluation.html',
            {
                'title':'List of Students',
                'descriptive_title' : 'View and shortlist Panel Sent by Guide For Final evaluation',
                'unread_notifications' : get_unread_notifications(request.session['username']),
                'all_list' : all_list
            }
        )
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def director_help_procedure(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    return render(
        request,
        'app/director/procedure.html',
        {
            'title':'Procedure',
            'descriptive_title' : 'PhD Evaluation Procedure',
            'unread_notifications' : get_unread_notifications(request.session['username'])
        }
    )

@login_required
def director_help_contacts(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    return render(
        request,
        'app/director/help_contacts.html',
        {
            'title':'Help Contacts',
            'descriptive_title' : 'Contacts for critical issues',
            'unread_notifications' : get_unread_notifications(request.session['username'])
        }
    )