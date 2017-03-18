"""
Definition of views.
"""

from app.login_views import *
from app.student_views import *
from app.guide_views import *
from app.director_views import *
from app.referee_views import *

def resource_not_found(request):
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/other/404.html',
        {
            'title':'Resource not found'
        }
    )

def unauthorized_access(request):
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/other/403.html',
        {
            'title':'Resource not found'
        }
    )