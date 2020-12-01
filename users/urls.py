from django.urls import path
from users.views import StaffListView, StaffCreateView, StaffUpdateView, StudentListView, StudentCreateView, StudentUpdateView


urlpatterns = [
    path('staff/', StaffListView.as_view(), name='list_staff'),
    path('staff/new/', StaffCreateView.as_view(), name='new_staff'),
    path('staff/edit/<int:pk>', StaffUpdateView.as_view(), name='edit_staff'),
    path('students/', StudentListView.as_view(), name='list_student'),
    path('students/new/', StudentCreateView.as_view(), name='new_student'),
    path('students/edit/<int:pk>', StudentUpdateView.as_view(), name='edit_student'),
]
