from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from .models import Feedback


class FeedbackAdminSite(AdminSite):
    pass


class FeedbackAdmin(admin.ModelAdmin):
    fields = ['subject', 'message', 'name', 'email', 'comment', 'link']
    list_display = ('subject', 'message', 'name', 'email', 'comment', 'link')

    def has_add_permission(self, request):
        return False

feedback_admin_site = FeedbackAdminSite(name='feedbackadmin')
feedback_admin_site.register(Feedback, FeedbackAdmin)
