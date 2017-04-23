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
from app import views, student_views, guide_views, referee_views, director_views, admin_views

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

    # admin urls
    url(r'^admin/reports/$', app.admin_views.admin_evaluate_reports, name='admin_evaluate_reports'),
    url(r'^admin/add/referee/$', app.admin_views.admin_add_referee, name='admin_add_referee'),
    url(r'^admin/approve/referee/$', app.admin_views.admin_approve_referee, name='admin_approve_referee'),
    url(r'^admin/Synopsis/$', app.admin_views.admin_view_request_for_synopsis, name='admin_view_request_for_synopsis'),
    url(r'^admin/Synopsis/evaluate/$', app.admin_views.admin_evaluate_request_for_synopsis, name='admin_evaluate_request_for_synopsis'),
    url(r'^admin/Synopsis/seminar/list/conduct/$', app.admin_views.admin_conductSeminar, name='admin_conductSeminar'),
    url(r'^admin/Synopsis/seminar/list/$', app.admin_views.admin_preSubmissionSeminars, name='admin_preSubmissionSeminars'),
    url(r'^admin/Synopsis/seminar/list/evaluate/$', app.admin_views.admin_preSubmissionSeminars_evaluate, name='admin_preSubmissionSeminars_evaluate'),
    url(r'^admin/Panel/$', app.admin_views.admin_panelapproval, name='admin_panelapproval'),
    url(r'^admin/Panel/upload/(?P<id>\d+)$', app.admin_views.admin_panel_upload, name='admin_panel_upload'),
    url(r'^admin/Panel/evaluate/$', app.admin_views.admin_panelapproval_evaluate, name='admin_panelapproval_evaluate'),
    url(r'^admin/Panel/print/(?P<id>\d+)$', app.admin_views.admin_panel_print, name='admin_panel_print'),

    # student urls
    url(r'^student/abstract/$', app.student_views.student_add_abstract, name='student_add_abstract'),
    url(r'^student/add/details/$', app.student_views.student_add_details, name='student_add_details'), 
    url(r'^student/synopsis/upload/$', app.student_views.student_upload_synopsis, name='student_upload_synopsis'),
    url(r'^student/request/synopsis/$', app.student_views.student_request_synopsis, name='student_request_synopsis'),
    url(r'^student/synopsis/view/$', app.student_views.student_view_synopsis, name='student_view_synopsis'),
    url(r'^student/thesis/upload/$', app.student_views.student_upload_thesis, name='student_upload_thesis'),
    url(r'^student/thesis/view/$', app.student_views.student_view_thesis, name='student_view_thesis'),
    url(r'^student/keywords/$', app.student_views.student_add_keywords, name='student_add_keywords'),
    url(r'^student/keywords/get/$', app.student_views.get_ieee_keywords, name='get_ieee_keywords'),
    url(r'^student/keywords/get/parent/$', app.student_views.get_ieee_keywords_parent, name='get_ieee_keywords_parent'),
    url(r'^student/keywords/delete/(?P<id>\d+)$', app.student_views.student_delete_keyword, name='student_delete_keyword'),
    url(r'^student/keywords/search/$', app.student_views.student_search_keywords, name='student_search_keywords'),
    url(r'^student/keywords/add/$', app.student_views.student_add_keyword_to_thesis, name='student_add_keyword_to_thesis'),
    url(r'^student/keywords/add/custom/$', app.student_views.student_add_custom_keyword, name='student_add_custom_keyword'),
    url(r'^student/keywords/recommendations/$', app.student_views.student_keyword_recommendations, name='student_keyword_recommendations'),
    url(r'^student/status/$', app.student_views.student_phd_status, name='student_phd_status'),
    url(r'^student/help/procedure/$', app.student_views.student_help_procedure, name='student_help_procedure'),
    url(r'^student/help/contacts/$', app.student_views.student_help_contacts, name='student_help_contacts'),

    # guide urls
    url(r'^guide/abstract/unevaluated/$', app.guide_views.guide_unevaluated_abstract, name='guide_unevaluated_abstract'),
    url(r'^guide/abstract/unevaluated/evaluate/$', app.guide_views.guide_evaluate_unevaluated_abstract),
    url(r'^guide/synopsis/unevaluated/$', app.guide_views.guide_unevaulated_synopsis, name='guide_unevaulated_synopsis'),
    
    url(r'^guide/add/referee/$', app.guide_views.guide_add_referee, name='guide_add_referee'),
    url(r'^guide/synopsis/unevaluated/evaluate/$', app.guide_views.guide_evaluate_unevaluated_synopsis),
    url(r'^guide/thesis/unevaluated/$', app.guide_views.guide_unevaluated_thesis, name='guide_unevaluated_thesis'),
    url(r'^guide/thesis/unevaluated/evaluate/$', app.guide_views.guide_evaluate_unevaluated_thesis),
    
    url(r'^guide/panel/$', app.guide_views.guide_submit_evaluation_panel, name='guide_submit_evaluation_panel'),
    url(r'^guide/panel/submit/$', app.guide_views.guide_send_panel_to_admin, name='guide_send_panel_to_admin'),
    url(r'^guide/panel/save/$', app.guide_views.guide_save_panel_members, name='guide_save_panel_members'),
    
    url(r'^guide/feedback/reports/$', app.guide_views.guide_feedback_reports, name='guide_feedback_reports'),
    url(r'^guide/feedback/reports/reevaluate/$', app.guide_views.guide_re_evaluate),
    url(r'^guide/feedback/reports/modifications/$', app.guide_views.guide_modifications),
    url(r'^guide/feedback/reports/vivavoice/$', app.guide_views.guide_viva_voice),

    url(r'^user/panel/referees/indian/$', app.guide_views.guide_get_indian_referee_details, name='guide_get_indian_referee_details'),
    url(r'^user/panel/referees/foreign/$', app.guide_views.guide_get_foreign_referee_details, name='guide_get_foreign_referee_details'),
    url(r'^guide/status/$', app.guide_views.guide_phd_status, name='guide_phd_status'),
    url(r'^guide/help/procedure/$', app.guide_views.guide_help_procedure, name='guide_help_procedure'),
    url(r'^guide/help/contacts/$', app.guide_views.guide_help_contacts, name='guide_help_contacts'),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', admin.site.urls),

    #Director urls
    url(r'^director/students/$', app.director_views.director_view_student_info, name='director_view_student_info'),
    url(r'^director/panel/add/$', app.director_views.director_add_panel_members, name='director_add_panel_members'),
    url(r'^director/evaluate/$', app.director_views.director_submit_for_evaluation, name='director_submit_for_evaluation'),
    url(r'^director/help/procedure/$', app.director_views.director_help_procedure, name='director_help_procedure'),
    url(r'^director/help/contacts/$', app.director_views.director_help_contacts, name='director_help_contacts'),

    #Referee urls
    #for password reset link		
	url(r'^reset/token=/(?P<token>.*)$', app.referee_views.validate_password_reset_link, name='validate_password_reset_link'),		
	url(r'^forgotpassword$', app.referee_views.forgotpassword, name='forgotpassword'),		
	url(r'^referee/change-forgot-password/$', app.referee_views.referee_change_forgot_password, name='referee_change_forgot_password'),
    url(r'^referee/change-password/$', app.referee_views.referee_change_password, name='referee_change_password'),
    url(r'^referee/synopsis/$', app.referee_views.referee_evaluate_synopsis, name='referee_evaluate_synopsis'),
    url(r'^referee/synopsis/evaluate/$', app.referee_views.referee_synopsis_approval),
    url(r'^referee/thesis/$', app.referee_views.referee_evaluate_thesis, name='referee_evaluate_thesis'),
    url(r'^referee/thesis/evaluate/$', app.referee_views.referee_thesis_approval ),
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