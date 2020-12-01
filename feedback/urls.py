from django.urls import path
from feedback.views import (
    StaffFeedbackCreateView, StaffFeedbackListView, StaffFeedbackUpdateView,
    StudentFeedbackCreateView, StudentFeedbackListView, StudentFeedbackUpdateView
)


urlpatterns = [
    path('staff/', StaffFeedbackCreateView.as_view(), name='new_staff'),
    path('admin/staff/', StaffFeedbackListView.as_view(), name='list_staff'),
    path('staff/update/<int:pk>', StaffFeedbackUpdateView.as_view(), name='update_staff'),
    path('student/', StudentFeedbackCreateView.as_view(), name='new_student'),
    path('admin/student/', StudentFeedbackListView.as_view(), name='list_student'),
    path('student/update/<int:pk>', StudentFeedbackUpdateView.as_view(), name='update_student'),
]
