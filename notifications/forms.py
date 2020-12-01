from django.forms import ModelForm
from notifications.models import NotificationStaff, NotificationStudent


class NotificationStaffForm(ModelForm):
    class Meta:
        model = NotificationStaff
        fields = ('staff', 'message')


class NotificationStudentForm(ModelForm):
    class Meta:
        model = NotificationStudent
        fields = ('student', 'message')
