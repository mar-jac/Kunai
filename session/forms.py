from django import forms
from django.forms import ModelForm
from session.models import Session


class DateInput(forms.DateInput):
    input_type = 'date'


class SessionForm(ModelForm):
    class Meta:
        model = Session
        fields = '__all__'
        widgets = {
            'start_year': DateInput(),
            'end_year': DateInput(),
        }
