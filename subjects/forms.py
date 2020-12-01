from django.forms import ModelForm
from subjects.models import Subject


class SubjectForm(ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'
