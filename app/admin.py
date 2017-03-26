from django.contrib import admin
from app.models import *

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email_id')
    search_fields = ('first_name', 'last_name', 'email_id')
    list_filter = ('type',)

class StatusTypesAdmin(admin.ModelAdmin):
    list_display = ('id', 'status_message',)
    search_fields = ('id', 'status_message',)

class ThesisAdmin(admin.ModelAdmin):
    list_display = ('title', 'username',)
    search_fields = ('title', 'abstract')
    list_filter = ('status',)
    
class ThesisGuidesAdmin(admin.ModelAdmin):
    list_display = ('guide_username', 'thesis_id',)
    search_fields = ('guide_username', 'thesis_id',)

class IEEEKeywordsAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'parent_keyword_id',)
    search_fields = ('keyword',)

class ThesisKeywordsAdmin(admin.ModelAdmin):
    list_display = ('thesis_id', 'keyword_id',)
    search_fields = ('thesis_id', 'keyword_id',)

class PanelMembersAdmin(admin.ModelAdmin):
    list_display = ('thesis_id', 'referee_username', 'status',)
    search_fields = ('thesis_id', 'referee_username',)
    list_filter = ('status',)

class NotificationsAdmin(admin.ModelAdmin):
    list_display = ('receiver', 'sender', 'message', 'status')
    search_fields = ('receiver', 'sender', 'message',)
    list_filter = ('status',)

class RefereesAdmin(admin.ModelAdmin):
    list_display = ('user', 'type')
    list_filter = ('type',)

admin.site.register(User, UserAdmin)
admin.site.register(StatusTypes, StatusTypesAdmin)
admin.site.register(Thesis, ThesisAdmin)
admin.site.register(ThesisGuides, ThesisGuidesAdmin)
admin.site.register(IEEEKeywords, IEEEKeywordsAdmin)
admin.site.register(ThesisKeywords, ThesisKeywordsAdmin)
admin.site.register(PanelMembers, PanelMembersAdmin)
admin.site.register(Notifications, NotificationsAdmin)
admin.site.register(Referees, RefereesAdmin)