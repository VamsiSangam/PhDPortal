"""
Definition of urls for PhD portal.
"""

from datetime import datetime
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
import django.contrib.auth.views
import app
from app import views, student_views, guide_views, referee_views, director_views

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # common urls
    url(r'^$', app.views.login, name='login'),
    url(r'^logout/$', app.views.logout, name='logout'),
    url(r'^user/profile/$', app.views.user_profile, name='user_profile'),
    url(r'^user/profile/(?P<username>[\w\d]+)/$', app.views.view_user_profile, name='view_user_profile'),
    url(r'^user/notifications/$', app.views.user_notifications, name='user_notifications'),
    url(r'^user/notifications/delete/(?P<id>\d+)$', app.views.delete_user_notification, name='delete_user_notification'),
    url(r'^user/notifications/delete/read/$', app.views.delete_all_read_notifications, name='delete_all_read_notifications'),
    url(r'^user/notifications/delete/unread/$', app.views.delete_all_unread_notifications, name='delete_all_unread_notifications'),
    url(r'^user/notifications/markread/all/$', app.views.mark_all_notifications_read, name='mark_all_notifications_read'),
    url(r'^user/notifications/markread/(?P<id>\d+)$', app.views.mark_notification_read, name='mark_notification_read'),
    url(r'^user/edit_profile/$', app.views.user_edit_profile, name='user_edit_profile'),
    url(r'^user/search/$', app.views.search_user, name='search_user'),
    url(r'^user/search/query/$', app.views.search_user_query, name='search_user_query'),

    # student urls
    url(r'^student/abstract/$', app.student_views.student_add_abstract, name='student_add_abstract'),  
    url(r'^student/synopsis/upload/$', app.student_views.student_upload_synopsis, name='student_upload_synopsis'),
    url(r'^student/synopsis/view/$', app.student_views.student_view_synopsis, name='student_view_synopsis'),
    url(r'^student/thesis/upload/$', app.student_views.student_upload_thesis, name='student_upload_thesis'),
    url(r'^student/thesis/view/$', app.student_views.student_view_thesis, name='student_view_thesis'),
    url(r'^student/keywords/$', app.student_views.student_add_keywords, name='student_add_keywords'),
    url(r'^student/keywords/get/$', app.student_views.get_ieee_keywords, name='get_ieee_keywords'),
    url(r'^student/keywords/get/parent/$', app.student_views.get_ieee_keywords_parent, name='get_ieee_keywords_parent'),
    url(r'^student/keywords/delete/(?P<id>\d+)$', app.student_views.student_delete_keyword, name='student_delete_keyword'),
    url(r'^student/keywords/add/$', app.student_views.student_add_keyword_to_thesis, name='student_add_keyword_to_thesis'),
    url(r'^student/status/$', app.student_views.student_phd_status, name='student_phd_status'),
    url(r'^student/help/procedure/$', app.student_views.student_help_procedure, name='student_help_procedure'),
    url(r'^student/help/contacts/$', app.student_views.student_help_contacts, name='student_help_contacts'),

    # guide urls
    url(r'^guide/abstract/unevaluated/$', app.guide_views.guide_unevaluated_abstract, name='guide_unevaluated_abstract'),
    url(r'^guide/abstract/unevaluated/evaluate/$', app.guide_views.guide_evaluate_unevaluated_abstract),
    url(r'^guide/synopsis/unevaluated/$', app.guide_views.guide_unevaulated_synopsis, name='guide_unevaulated_synopsis'),
    url(r'^guide/synopsis/unevaluated/evaluate/$', app.guide_views.guide_evaluate_unevaluated_synopsis),
    url(r'^guide/thesis/unevaluated/$', app.guide_views.guide_unevaluated_thesis, name='guide_unevaluated_thesis'),
    url(r'^guide/thesis/unevaluated/evaluate/$', app.guide_views.guide_evaluate_unevaluated_thesis),
    url(r'^guide/panel/$', app.guide_views.guide_submit_evaluation_panel, name='guide_submit_evaluation_panel'),
    url(r'^guide/panel/submit/$', app.guide_views.guide_add_referee_panel_members, name='guide_add_referee_panel_members'),
    url(r'^guide/panel/referees/indian/$', app.guide_views.guide_get_indian_referee_details, name='guide_get_indian_referee_details'),
    url(r'^guide/panel/referees/foreign/$', app.guide_views.guide_get_foreign_referee_details, name='guide_get_foreign_referee_details'),
    url(r'^guide/panel/pending/$', app.guide_views.guide_pending_evaluation_panels, name='guide_pending_evaluation_panels'),

    url(r'^guide/panel/pending/approve/$', app.guide_views.guide_approve_panel_members, name='guide_approve_panel_members'),
    url(r'^guide/panel/pending/reject/$', app.guide_views.guide_reject_panel_members, name='guide_reject_panel_members'),
    url(r'^guide/panel/pending/edit/$', app.guide_views.guide_edit_panel_members, name='guide_edit_panel_members'),

    url(r'^guide/status/$', app.guide_views.guide_phd_status, name='guide_phd_status'),
    url(r'^guide/help/procedure/$', app.guide_views.guide_help_procedure, name='guide_help_procedure'),
    url(r'^guide/help/contacts/$', app.guide_views.guide_help_contacts, name='guide_help_contacts'),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', admin.site.urls),

    #Director urls
    url(r'^director/$', app.director_views.director_home, name='director_home'), 
    url(r'^director/students/$', app.director_views.director_view_student_info, name='director_view_student_info'),
    url(r'^director/evaluate/$', app.director_views.director_submit_for_evaluation, name='director_submit_for_evaluation'),
    url(r'^director/help/procedure/$', app.director_views.director_help_procedure, name='director_help_procedure'),
    url(r'^director/help/contacts/$', app.director_views.director_help_contacts, name='director_help_contacts'),

    #Referee urls
    url(r'^referee/$', app.referee_views.referee_home, name='referee_home'),   
    url(r'^referee/requestedlist/$', app.referee_views.referee_requestedlist, name='referee_requestedlist'),
    url(r'^referee/evaluate/thesis/$', app.referee_views.referee_evaluation, name='referee_evaluation'),
    url(r'^referee/evaluate/feedback/$', app.referee_views.referee_evaluation_report, name='referee_evaluation_report'),
    url(r'^referee/help/procedure/$', app.referee_views.referee_help_procedure, name='referee_help_procedure'),
    url(r'^referee/help/contacts/$', app.referee_views.referee_help_contacts, name='referee_help_contacts'),

    # other
    url(r'^400/$', app.views.bad_request, name='bad_request'),
    url(r'^401/$', app.views.unauthorized_access, name='unauthorized_access'),
    url(r'^403/$', app.views.forbidden, name='forbidden'),
    url(r'^404/$', app.views.not_found, name='not_found'),    
    url(r'^500/$', app.views.internal_server_error, name='internal_server_error'),
    url(r'[a-zA-Z0-9]*', app.views.not_found),
    ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)