from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from .models import Feedback


class FeedbackAdminSite(AdminSite):
    pass


class FeedbackAdmin(admin.ModelAdmin):
    fields = ['subject', 'message', 'name', 'email', 'comment', 'link', 'date_created']
    list_display = ('subject', 'message', 'name', 'email', 'comment', 'link', 'date_created')

    def has_add_permission(self, request):
        return False


feedback_admin = FeedbackAdminSite(name='feedbackadmin')
feedback_admin.register(Feedback, FeedbackAdmin)
print(feedback_admin.get_urls())
