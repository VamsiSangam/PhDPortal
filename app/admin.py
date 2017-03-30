from django.contrib import admin
from app.models import *

# Classes used for Django admin functionalities

class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'section_slug',)
    search_fields = ('name',)

class AppAdmin(admin.ModelAdmin):
    list_display = ('name', 'section',)
    search_fields = ('name', 'section',)

class MenuTemplateAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'url',)
    search_fields = ('name',)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'salutation',)
    search_fields = ('user',)
    list_filter = ('gender',)

class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'type',)
    search_fields = ('name', 'department')
    list_filter = ('department', 'type')

class AdmissionBatchAdmin(admin.ModelAdmin):
    list_display = ('program', 'admission_year', 'session', 'enrollment_prefix',)
    search_fields = ('program', 'admission_year', 'session', 'enrollment_prefix',)

class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'current_batch',)
    search_fields = ('first_name', 'last_name', 'middle_name', 'current_roll_no')
    list_filter = ('category',)

class FacultyAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'designation',)
    search_fields = ('first_name', 'last_name', 'middle_name', 'designation')
    list_filter = ('designation',)

class StateAdmin(admin.ModelAdmin):
    list_display = ('name', 'code',)
    search_fields = ('name', 'code',)

class CommunicationAddressAdmin(admin.ModelAdmin):
    list_display = ('referee', 'address_line1', 'address_line2', 'city',)
    search_fields = ('referee', 'address_line1', 'address_line2', 'city',)
    list_filter = ('city', 'type',)

class RefereeAdmin(admin.ModelAdmin):
    list_display = ('user', 'university', 'designation', 'website',)
    search_fields = ('user', 'university', 'designation', 'website',)
    list_filter = ('type',)

class ApproverAdmin(admin.ModelAdmin):
    list_display = ('faculty', 'active')
    search_fields = ('faculty', 'active')

class StatusTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'status_message',)
    search_fields = ('id', 'status_message',)

class ThesisAdmin(admin.ModelAdmin):
    list_display = ('title', 'student',)
    search_fields = ('title', 'student', 'abstract')
    list_filter = ('status',)
    
class ThesisGuideAdmin(admin.ModelAdmin):
    list_display = ('guide', 'thesis', 'type')
    search_fields = ('guide', 'thesis',)

class IEEEKeywordAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'parent',)
    search_fields = ('keyword',)

class ThesisKeywordAdmin(admin.ModelAdmin):
    list_display = ('thesis', 'keyword',)
    search_fields = ('thesis', 'keyword',)

class PanelMemberAdmin(admin.ModelAdmin):
    list_display = ('thesis', 'referee', 'status',)
    search_fields = ('thesis', 'referee',)
    list_filter = ('status',)

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('receiver', 'sender', 'message', 'status')
    search_fields = ('receiver', 'sender', 'message',)
    list_filter = ('status',)

# Registering classes to Django admin
admin.site.register(Section, SectionAdmin)
admin.site.register(App, AppAdmin)
admin.site.register(MenuTemplate, MenuTemplateAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Program, ProgramAdmin)
admin.site.register(AdmissionBatch, AdmissionBatchAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(CommunicationAddress, CommunicationAddressAdmin)
admin.site.register(Referee, RefereeAdmin)
admin.site.register(Approver, ApproverAdmin)
admin.site.register(StatusType, StatusTypeAdmin)
admin.site.register(Thesis, ThesisAdmin)
admin.site.register(ThesisGuide, ThesisGuideAdmin)
admin.site.register(IEEEKeyword, IEEEKeywordAdmin)
admin.site.register(ThesisKeyword, ThesisKeywordAdmin)
admin.site.register(PanelMember, PanelMemberAdmin)
admin.site.register(Notification, NotificationAdmin)


## Define an inline admin descriptor for Employee model
## which acts a bit like a singleton
#class StudentInline(admin.StackedInline):
#    model = Student
#    can_delete = False
#    verbose_name_plural = 'students'

#class FacultyInline(admin.StackedInline):
#    model = Faculty
#    can_delete = False
#    verbose_name_plural = 'faculties'

#class RefereeInline(admin.StackedInline):
#    model = Referee
#    can_delete = False
#    verbose_name_plural = 'referees'

## Define a new User admin
#class UserAdmin(BaseUserAdmin):
#    inlines = (StudentInline, FacultyInline, RefereeInline)

## Re-register UserAdmin
#admin.site.unregister(User)
#admin.site.register(User, UserAdmin)