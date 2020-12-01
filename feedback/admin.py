from django.contrib import admin
from feedback.models import FeedbackStudent, FeedbackStaff


admin.site.register(FeedbackStudent)
admin.site.register(FeedbackStaff)
