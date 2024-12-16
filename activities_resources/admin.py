from django.contrib import admin

from .models import Activity, Resource, AssignedActivity, ActivityProgress

class ActivityAdmin(admin.ModelAdmin):
    pass
    #list_display = ('email','role')

class ResourceAdmin(admin.ModelAdmin):
    pass
    #list_display = ('user', 'career')
    
class AssignedActivityAdmin(admin.ModelAdmin):
    pass
    #list_display = ('email','role')
    
class ActivityProgressAdmin(admin.ModelAdmin):
    pass
    #list_display = ('email','role')


admin.site.register(Activity, ActivityAdmin)
admin.site.register(Resource, ResourceAdmin)
admin.site.register(AssignedActivity, AssignedActivityAdmin)
admin.site.register(ActivityProgress, ActivityProgressAdmin)
