from django.contrib import admin
from users.models import User, Profile


class UserAdmin(admin.ModelAdmin):
    list_display = ('email','role')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'career')

admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)