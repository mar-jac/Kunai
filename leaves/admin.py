from django.contrib import admin
from leaves.models import LeaveReportStudent, LeaveReportStaff


admin.site.register(LeaveReportStudent)
admin.site.register(LeaveReportStaff)
