from django.contrib import admin

from xrp.userprofile.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserProfile, UserProfileAdmin)
