from django.urls import path
from leaves.views import (
    StaffLeaveCreateView, StaffLeaveListView, StaffLeaveUpdateView,
    StudentLeaveCreateView, StudentLeaveListView, StudentLeaveUpdateView
)


urlpatterns = [
    path('staff/', StaffLeaveCreateView.as_view(), name='new_staff'),
    path('admin/staff/', StaffLeaveListView.as_view(), name='list_staff'),
    path('staff/update/<int:pk>', StaffLeaveUpdateView.as_view(), name='update_staff'),
    path('student/', StudentLeaveCreateView.as_view(), name='new_student'),
    path('admin/student/', StudentLeaveListView.as_view(), name='list_student'),
    path('student/update/<int:pk>', StudentLeaveUpdateView.as_view(), name='update_student'),
]
