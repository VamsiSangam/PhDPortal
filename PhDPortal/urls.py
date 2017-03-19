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
    # common urls
    url(r'^$', app.views.login, name='login'),
    url(r'^logout/$', app.views.logout, name='logout'),
    url(r'^notifications/$', app.views.user_notifications, name='user_notifications'),
    url(r'^notifications/delete/(?P<id>\d+)$', app.views.delete_user_notification, name='delete_user_notification'),
    url(r'^notifications/delete/read/$', app.views.delete_all_read_notifications, name='delete_all_read_notifications'),
    url(r'^notifications/delete/unread/$', app.views.delete_all_unread_notifications, name='delete_all_unread_notifications'),
    url(r'^notifications/markread/all/$', app.views.mark_all_notifications_read, name='mark_all_notifications_read'),
    url(r'^notifications/markread/(?P<id>\d+)$', app.views.mark_notification_read, name='mark_notification_read'),
    url(r'^edit_profile/$', app.views.user_edit_profile, name='user_edit_profile'),

    # student urls
    url(r'^student/$', app.views.student_home, name='student_home'),  
    url(r'^student/synopsis/upload/$', app.views.student_upload_synopsis, name='student_upload_synopsis'),
    url(r'^student/synopsis/view/$', app.views.student_view_synopsis, name='student_view_synopsis'),
    url(r'^student/thesis/upload/$', app.views.student_upload_thesis, name='student_upload_thesis'),
    url(r'^student/thesis/view/$', app.views.student_view_thesis, name='student_view_thesis'),
    url(r'^student/keywords/$', app.views.student_add_keywords, name='student_add_keywords'),
    url(r'^student/keywords/get/$', app.views.get_ieee_keywords, name='get_ieee_keywords'),
    url(r'^student/keywords/get/parent/$', app.views.get_ieee_keywords_parent, name='get_ieee_keywords_parent'),
    url(r'^student/keywords/delete/(?P<id>\d+)$', app.views.student_delete_keyword, name='student_delete_keyword'),
    url(r'^student/keywords/add/$', app.views.student_add_keyword_to_thesis, name='student_add_keyword_to_thesis'),
    url(r'^student/status/$', app.views.student_phd_status, name='student_phd_status'),
    url(r'^student/help/procedure/$', app.views.student_help_procedure, name='student_help_procedure'),
    url(r'^student/help/contacts/$', app.views.student_help_contacts, name='student_help_contacts'),

    # guide urls
    url(r'^guide/$', app.views.guide_home, name='guide_home'),   
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
    url(r'^director/students/$', app.views.director_view_student_info, name='director_view_student_info'),
    url(r'^director/evaluate/$', app.views.director_submit_for_evaluation, name='director_submit_for_evaluation'),
    url(r'^director/help/procedure/$', app.views.director_help_procedure, name='director_help_procedure'),
    url(r'^director/help/contacts/$', app.views.director_help_contacts, name='director_help_contacts'),

    #Referee urls
    url(r'^referee/$', app.views.referee_home, name='referee_home'),   
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