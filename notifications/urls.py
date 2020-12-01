from django.urls import path
from notifications.views import (
    StaffNotificationCreateView, StudentNotificationCreateView,
    StaffNotificationListView, StudentNotificationListView,
    StaffNotificationUpdateView, StudentNotificationUpdateView
)


urlpatterns = [
    path('staff/', StaffNotificationListView.as_view(), name='list_staff'),
    path('student/', StudentNotificationListView.as_view(), name='list_student'),
    path('staff/new/', StaffNotificationCreateView.as_view(), name='new_staff'),
    path('student/new/', StudentNotificationCreateView.as_view(), name='new_student'),
    path('staff/update/<int:pk>/', StaffNotificationUpdateView.as_view(), name='update_staff'),
    path('student/update/<int:pk>/', StudentNotificationUpdateView.as_view(), name='update_student'),
]
