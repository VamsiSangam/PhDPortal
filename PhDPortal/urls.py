"""
Definition of urls for DjangoWebProject2.
"""

from datetime import datetime
from django.conf.urls import url
from django.contrib import admin
import django.contrib.auth.views

import app.forms
import app.views

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    url(r'^$', app.views.login, name='login'),
    url(r'^logout/$', app.views.logout, name='logout'),
    
    # student urls
    url(r'^student/$', app.views.student_home, name='student_home'),
    url(r'^student/notifications/$', app.views.student_all_notifications, name='student_all_notifications'),    
    url(r'^student/profile/edit/$', app.views.student_edit_profile, name='student_edit_profile'),
    url(r'^student/synopsis/upload/$', app.views.student_upload_synopsis, name='student_upload_synopsis'),
    url(r'^student/synopsis/view/$', app.views.student_view_synopsis, name='student_view_synopsis'),
    url(r'^student/thesis/upload/$', app.views.student_upload_thesis, name='student_upload_thesis'),
    url(r'^student/thesis/view/$', app.views.student_view_thesis, name='student_view_thesis'),
    url(r'^student/keywords/$', app.views.student_add_keywords, name='student_add_keywords'),
    url(r'^student/status/$', app.views.student_phd_status, name='student_phd_status'),
    url(r'^student/help/procedure/$', app.views.student_help_procedure, name='student_help_procedure'),
    url(r'^student/help/contacts/$', app.views.student_help_contacts, name='student_help_contacts'),

    # guide urls
    url(r'^guide/$', app.views.guide_home, name='guide_home'),
    url(r'^guide/notifications/$', app.views.guide_all_notifications, name='guide_all_notifications'),    
    url(r'^guide/profile/edit/$', app.views.guide_edit_profile, name='guide_edit_profile'),
    url(r'^guide/students/$', app.views.guide_view_student_info, name='guide_view_student_info'),
    url(r'^guide/synopsis/unevaluated/$', app.views.guide_unevaulated_synopsis, name='guide_unevaulated_synopsis'),
    url(r'^guide/synopsis/archived/$', app.views.guide_archived_synopsis, name='guide_archived_synopsis'),
    url(r'^guide/thesis/unevaluated/$', app.views.guide_unevaluated_thesis, name='guide_unevaluated_thesis'),
    url(r'^guide/thesis/archived/$', app.views.guide_archived_thesis, name='guide_archived_thesis'),
    url(r'^guide/status/$', app.views.guide_phd_status, name='guide_phd_status'),
    url(r'^guide/help/procedure/$', app.views.guide_help_procedure, name='guide_help_procedure'),
    url(r'^guide/help/contacts/$', app.views.guide_help_contacts, name='guide_help_contacts'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', admin.site.urls),

    #Director urls
    url(r'^director/$', app.views.director_home, name='director_home'),
    url(r'^director/notifications/$', app.views.director_all_notifications, name='director_all_notifications'),    
    url(r'^director/profile/edit/$', app.views.director_edit_profile, name='director_edit_profile'),
    url(r'^director/students/$', app.views.director_view_student_info, name='director_view_student_info'),
    url(r'^director/evaluate/$', app.views.director_submit_for_evaluation, name='director_submit_for_evaluation'),
    url(r'^director/help/procedure/$', app.views.director_help_procedure, name='director_help_procedure'),
    url(r'^director/help/contacts/$', app.views.director_help_contacts, name='director_help_contacts'),

    #Referee urls
    url(r'^referee/$', app.views.referee_home, name='referee_home'),
    url(r'^referee/notifications/$', app.views.referee_all_notifications, name='referee_all_notifications'),    
    url(r'^referee/profile/edit/$', app.views.referee_edit_profile, name='referee_edit_profile'),
    url(r'^referee/requestedlist/$', app.views.referee_requestedlist, name='referee_requestedlist'),
    url(r'^referee/evaluate/thesis/$', app.views.referee_evaluation, name='referee_evaluation'),
    url(r'^referee/evaluate/feedback/$', app.views.referee_evaluation_report, name='referee_evaluation_report'),
    url(r'^referee/help/procedure/$', app.views.referee_help_procedure, name='referee_help_procedure'),
    url(r'^referee/help/contacts/$', app.views.referee_help_contacts, name='referee_help_contacts'),

    # other
    url(r'^404/$', app.views.resource_not_found, name='resource_not_found'),
    url(r'^403/$', app.views.unauthorized_access, name='unauthorized_access'),
    url(r'[a-zA-Z0-9]*', app.views.resource_not_found, name='resource_not_found'),
    ]