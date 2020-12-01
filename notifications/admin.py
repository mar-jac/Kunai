from django.contrib import admin
from notifications.models import NotificationStudent, NotificationStaff


admin.site.register(NotificationStudent)
admin.site.register(NotificationStaff)
