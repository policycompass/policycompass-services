from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from .models import Feedback

class FeedbackAdminSite(AdminSite):
    fields = ['subject', 'message', 'name', 'email', 'comment']
    list_display = ('subject', 'message', 'name', 'email','comment')
class FeedbackAdmin(admin.ModelAdmin):
    fields = ['subject', 'message', 'name', 'email','comment']
    list_display = ('subject', 'message', 'name', 'email','comment')

feedback_admin_site = FeedbackAdminSite(name='feedbackadmin')
feedback_admin_site.register(Feedback, FeedbackAdmin)
