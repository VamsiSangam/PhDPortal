from app.views import *

URL_STUDENT_ADD_ABSTRACT = 'student_add_abstract'
URL_STUDENT_VIEW_THESIS = 'student_view_thesis'
URL_STUDENT_ADD_KEYWORDS = 'student_add_keywords'

@login_required
def student_home(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    return render(
        request,
        'app/student/home.html',
        {
            'title':'Home Page',
            'descriptive_title' : 'Welcome ' + request.session['first_name'] + ' !',
            'unread_notifications' : get_unread_notifications(request.session['username']),
        }
    )

@login_required
def student_add_abstract(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))
    user = User.objects.get(username = request.session['username'])
    thesis = Thesis.objects.get(username = user)

    if request.method == "GET":
        abstract = thesis.abstract

        return render(request, 'app/student/phd_abstract.html', {
            'title' : 'PhD Abstract',
            'descriptive_title': 'Submit an Abstract for your PhD Thesis',
            'unread_notifications' : get_unread_notifications(request.session['username']),
            'abstract' : abstract
        })
    elif request.method == "POST":
        abstract = request.POST['abstract']
        thesis.abstract = abstract
        thesis.save()

        return redirect(reverse(URL_STUDENT_ADD_ABSTRACT))
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def student_upload_synopsis(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))
    user = User.objects.get(username = request.session['username'])
    thesis = Thesis.objects.get(username = user)

    if request.method == 'GET':
        synopsisExists = False

        if thesis.synopsis is not None:
            synopsisExists = True

        return render(
            request,
            'app/student/upload_synopsis.html',
            {   
                'title' : 'Upload Synopsis',
                'descriptive_title' : 'Upload a Synopsis of your PhD',
                'unread_notifications' : get_unread_notifications(request.session['username']),
                'synopsisExists' : synopsisExists 
            }
        )
    elif request.method == "POST":
        form = SynopsisForm(request.POST, request.FILES)
        
        if form.is_valid() and validate_pdf(request.FILES['synopsis']):
            thesis.synopsis = request.FILES['synopsis']
            thesis.save()
 
            return redirect(reverse('student_view_synopsis'))
        else:
            return redirect(reverse(URL_BAD_REQUEST))
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def student_view_synopsis(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    if request.method == "GET":
        user = User.objects.get(username = request.session['username'])
        thesis = Thesis.objects.get(username = user)
        synopsisPath = None

        if thesis.synopsis is not None:
            synopsisPath = thesis.synopsis

        return render(
            request,
            'app/student/view_synopsis.html',
            {
                'title':'View Synopsis',
                'descriptive_title' : 'View your submitted synopsis',
                'unread_notifications' : get_unread_notifications(request.session['username']),
                'synopsisPath' : synopsisPath
            }
        )
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def student_upload_thesis(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))
    user = User.objects.get(username = request.session['username'])
    thesis = Thesis.objects.get(username = user)

    if request.method == "GET":
        thesisExists = thesis.thesis is None

        return render(
            request,
            'app/student/upload_thesis.html',
            {
                'title':'Upload Thesis',
                'descriptive_title' : 'Upload PhD Thesis',
                'unread_notifications' : get_unread_notifications(request.session['username']),
                'thesisExists' : thesisExists
            }
        )
    elif request.method == "POST":
        form = ThesisForm(request.POST, request.FILES)
        
        if form.is_valid() and validate_pdf(request.FILES['thesis']):    
            thesis.thesis = request.FILES['thesis']
            thesis.save()
 
            return redirect(reverse(URL_STUDENT_VIEW_THESIS))
        else:
            return redirect(reverse(URL_BAD_REQUEST))
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def student_view_thesis(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    if request.method == "GET":
        user = User.objects.get(username = request.session['username'])
        thesis = Thesis.objects.get(username = user)
        thesisPath = thesis.thesis

        return render(
            request,
            'app/student/view_thesis.html',
            {
                'title':'View Thesis',
                'descriptive_title' : 'View you submitted PhD thesis',
                'unread_notifications' : get_unread_notifications(request.session['username']),
                'thesisPath' : thesisPath
            }
        )
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def student_add_keywords(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    if request.method == "GET":
        user = User.objects.get(username = request.session['username'])
        thesis = Thesis.objects.get(username = user)
        thesis_keywords = ThesisKeywords.objects.filter(thesis_id = thesis)

        return render(
            request,
            'app/student/add_keywords.html',
            {
                'title':'Add Keywords',
                'descriptive_title' : 'Add keywords to your PhD thesis',
                'unread_notifications' : get_unread_notifications(request.session['username']),
                'thesis' : thesis,
                'thesis_keywords' : thesis_keywords,
            }
        )
    else:
        return redirect(reverse(URL_BAD_REQUEST))

def _validate_keyword(id, username):
    thesis_keyword = ThesisKeywords.objects.get(id = id)

    if thesis_keyword is not None:
        if thesis_keyword.thesis_id.username.username == username:
            return True

    return False

@login_required
def student_delete_keyword(request, id):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))
    
    if request.method == "POST":
        if _validate_keyword(id, request.session['username']):
            thesis_keyword = ThesisKeywords.objects.get(id = id)
            thesis_keyword.delete()

            return redirect(reverse(URL_STUDENT_ADD_KEYWORDS))
        else:
            return redirect(reverse(URL_FORBIDDEN))
    else:
        return redirect(reverse(URL_BAD_REQUEST))

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

@login_required
def get_ieee_keywords(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

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
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def get_ieee_keywords_parent(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))
    
    if (request.method == "POST"):
        keyword = IEEEKeywords.objects.get(id = request.POST['parent_id'])
        id = keyword.parent_id.id

        if id is None:
            id = -1

        return HttpResponse(id, content_type = 'text/plain')
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def student_add_keyword_to_thesis(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

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

                return redirect(reverse(URL_STUDENT_ADD_KEYWORDS))
        else:
            return redirect(reverse(URL_FORBIDDEN))
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def student_phd_status(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    if request.method == "GET":
        return render(
            request,
            'app/student/phd_status.html',
            {
                'title':'PhD Thesis Submission Status',
                'descriptive_title' : 'PhD Thesis Submission Status',
                'unread_notifications' : get_unread_notifications(request.session['username']),
            }
        )
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def student_help_procedure(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    if request.method == "GET":
        return render(
            request,
            'app/student/procedure.html',
            {
                'title':'Procedure',
                'descriptive_title' : 'Having doubts about the submission procedure?',
                'unread_notifications' : get_unread_notifications(request.session['username']),
            }
        )
    else:
        return redirect(reverse(URL_BAD_REQUEST))

@login_required
def student_help_contacts(request):
    if not validate_request(request): return redirect(reverse(URL_FORBIDDEN))

    if request.method == "GET":
        return render(
            request,
            'app/student/help_contacts.html',
            {
                'title':'Help Contacts',
                'descriptive_title' : 'Contacts for critical issues',
                'unread_notifications' : get_unread_notifications(request.session['username']),
            }
        )
    else:
        return redirect(reverse(URL_BAD_REQUEST))