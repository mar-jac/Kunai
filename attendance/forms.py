from django import forms
from django.forms import ModelForm
from attendance.models import Attendance


class DateInput(forms.DateInput):
    input_type = 'date'


class AttendanceForm(ModelForm):
    def __init__(self, *args, **kwargs):
        staff = kwargs.pop('staff', None)
        super().__init__(*args, **kwargs)
        if staff:
            self.fields['subject'].queryset = staff.subject_set.all()

    class Meta:
        model = Attendance
        fields = '__all__'
        widgets = {
            'attendance_date': DateInput(),
        }


class AttendanceUpdateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        staff = kwargs.pop('staff', None)
        super().__init__(*args, **kwargs)
        if staff:
            self.fields['subject'].queryset = staff.subject_set.all()
            self.fields['attendance_date'] = forms.ChoiceField(choices=(('', '---------'),), label='Attendance Date')

    class Meta:
        model = Attendance
        fields = '__all__'


class AttendanceSearchForm(ModelForm):
    start_date = forms.DateField(widget=DateInput)
    end_date = forms.DateField(widget=DateInput)

    def __init__(self, *args, **kwargs):
        course = kwargs.pop('course', None)
        super().__init__(*args, **kwargs)
        if course:
            self.fields['subject'].queryset = course.subject_set.all()

    class Meta:
        model = Attendance
        fields = ('subject', 'start_date', 'end_date')
        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput()
        }
