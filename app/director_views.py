from app.views import *
from app.student_views import *

@login_required
def director_view_student_info(request):
    """
    View method. Renders student info page
    """

    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    if request.method == "GET":
        all_thesis = []     # list of dict
        for thesis in Thesis.objects.all():
            dict = {}
            dict['title'] = thesis.title
            dict['student_full_name'] = thesis.student.first_name + " " + thesis.student.last_name
            dict['student_username'] = thesis.student.user.username
            dict['id'] = thesis.id
            dict['status_message'] = thesis.status.status_message
            all_thesis.append(dict)
        return render(
            request,
            'app/director/view_student_info.html',
            {
                'title':'PhD Status',
                'layout_data' : get_layout_data(request),
                'all_thesis' : all_thesis
            }
        )
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def director_submit_for_evaluation(request):
    """
    View method. Renders page for director to choose panel
    """
    
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))
    
    if request.method == "GET": # post only for testing
        all_list = []     # list of dict
        for thesis in Thesis.objects.all():
            this_thesis = {}

            #need to use one more status if referees are out of bound
            if thesis.status.id >= STATUS_ID_PANEL_APPROVED and thesis.status.id < STATUS_ID_THESIS_UNDER_EVALUATION:
                #storing thesis information
                this_thesis['id'] = thesis.id
                this_thesis['username'] = thesis.student.user.username
                this_thesis['fullname'] = thesis.student.first_name + " " + thesis.student.last_name
                this_thesis['title'] = thesis.title
                this_thesis['abstract'] = thesis.abstract
                this_thesis['guides'] = []
                #storing guides of a thesis
                for thesis_guides in ThesisGuide.objects.filter(thesis = thesis):
                    dict = {}
                    dict['username'] = thesis_guides.guide.user.username
                    dict['fullname'] = thesis_guides.guide.first_name + " " + thesis_guides.guide.last_name
                    if thesis_guides.guide.type == 'G':
                        dict['type'] = 'Guide'
                    else:
                        dict['type'] = 'Co-Guide'
                    this_thesis['guides'].append(dict)
                #storing referee information
                this_thesis['indian_referees'] = []
                this_thesis['foreign_referees'] = []
                this_thesis['total_indian_panel'] = 0
                this_thesis['total_foreign_panel'] = 0

                for panel in PanelMember.objects.filter(thesis = thesis).filter(status = 'A'): #if the panel is approved(A) only
                    dict = {}
                    dict['username'] = panel.referee.user.username
                    dict['fullname'] = panel.referee.user.first_name + " " + panel.referee.user.last_name
                    dict['address'] = ' ajdnsands ' # leaving blank for now
                    referee = panel.referee
                    if referee.type == 'I':
                        dict['type'] = 'Indian'
                        this_thesis['indian_referees'].append(dict)
                    else:
                        dict['type'] = 'Foreign'
                        this_thesis['foreign_referees'].append(dict)
                #storing thesis keywords
                this_thesis['keywords'] = []
                
                for keys in ThesisKeyword.objects.filter(thesis = thesis):
                    this_thesis['keywords'].append((IEEEKeyword.objects.get(id = keys.keyword.id)).keyword)
                
                this_thesis['required_indian'] = INDIAN_REFEREES
                this_thesis['required_foreign'] = FOREIGN_REFEREES

                #for finalpanel in FinalPanel.objects.filter(thesis = thesis):
                #    referee = Referees.objects.get(user = finalpanel.referee_username)
                #    if referee.type == 'I' and finalpanel.status == 'Approved':
                #        this_thesis['required_indian'] -= 1
                #    if referee.type == 'F' and finalpanel.status == 'Approved':
                #        this_thesis['required_foreign'] -= 1
                all_list.append(this_thesis)
             
        return render(
            request,
            'app/director/submit_for_evaluation.html',
            {
                'title':'List of Students',
                'layout_data' : get_layout_data(request),
                'all_list' : all_list
            }
        )
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def director_help_procedure(request):
    """
    View method. Renders procedure help page.
    """

    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    return render(
        request,
        'app/director/procedure.html',
        {
            'title':'Procedure',
            'layout_data' : get_layout_data(request),
        }
    )

@login_required
def director_help_contacts(request):
    """
    View method. Renders contact help page.
    """

    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    return render(
        request,
        'app/director/help_contacts.html',
        {
            'title':'Help Contacts',
            'layout_data' : get_layout_data(request),
        }
    )