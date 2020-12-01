from django import forms
from django.forms import ModelForm
from feedback.models import FeedbackStaff, FeedbackStudent


class StaffFeedbackForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['feedback'].widget.attrs['rows'] = 4

    class Meta:
        model = FeedbackStaff
        fields = ('feedback',)


class StudentFeedbackForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['feedback'].widget.attrs['rows'] = 4

    class Meta:
        model = FeedbackStudent
        fields = ('feedback',)


class StaffReplyForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['reply'].widget.attrs['rows'] = 4

    class Meta:
        model = FeedbackStaff
        fields = ('reply',)


class StudentReplyForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['reply'].widget.attrs['rows'] = 4

    class Meta:
        model = FeedbackStudent
        fields = ('reply',)
