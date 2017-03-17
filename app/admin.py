from django.contrib import admin
from app.models import *

# Register your models here.
admin.site.register(User)
admin.site.register(StatusTypes)
admin.site.register(Thesis)

class ThesisGuidesAdmin(admin.ModelAdmin):
    list_display = ('guide_username', 'thesis_id',)

admin.site.register(ThesisGuides, ThesisGuidesAdmin)
admin.site.register(IEEEKeywords)
admin.site.register(ThesisKeywords)
admin.site.register(PanelMembers)
admin.site.register(Notifications)