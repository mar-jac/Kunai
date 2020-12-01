from django.urls import path
from attendance.views import AttendanceCreateView, AttendanceDetailView, AttendanceUpdateView, AttendanceStudentView


urlpatterns = [
    path('new/', AttendanceCreateView.as_view(), name='new'),
    path('', AttendanceDetailView.as_view(), name='detail'),
    path('update/', AttendanceUpdateView.as_view(), name='update'),
    path('search/', AttendanceStudentView.as_view(), name='search')
]
