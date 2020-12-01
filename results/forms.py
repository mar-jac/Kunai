from django import forms
from django.forms import ModelForm
from results.models import Result
from session.models import Session
from users.models import Student


class ResultForm(ModelForm):
    session = forms.ModelChoiceField(queryset=Session.objects.all(), required=True)

    def __init__(self, *args, **kwargs):
        staff = kwargs.pop('staff', None)
        super().__init__(*args, **kwargs)
        if staff:
            self.fields['subject'].queryset = staff.subject_set.all()
            self.fields['student'].queryset = Student.objects.none()

    class Meta:
        model = Result
        exclude = ('__all__',)
