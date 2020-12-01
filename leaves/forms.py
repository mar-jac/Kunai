from django import forms
from django.forms import ModelForm
from leaves.models import LeaveReportStaff, LeaveReportStudent


class DateInput(forms.DateInput):
    input_type = 'date'


class StaffLeaveForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['leave_message'].widget.attrs['rows'] = 4

    class Meta:
        model = LeaveReportStaff
        fields = ('leave_date', 'leave_message')
        widgets = {
            'leave_date': DateInput(),
        }


class StudentLeaveForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['leave_message'].widget.attrs['rows'] = 4

    class Meta:
        model = LeaveReportStudent
        fields = ('leave_date', 'leave_message')
        widgets = {
            'leave_date': DateInput(),
        }
