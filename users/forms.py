from django import forms
from django.forms import ModelForm
from users.models import CustomUser, Staff, Student
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError


class UserStaffForm(ModelForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['autofocus'] = True

    def save(self, commit=True, **kwargs):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.user_type = 2
        if commit:
            user.save()
            user.staff.address = kwargs['form'].cleaned_data['address']
            user.save()
        return user

    def _post_clean(self):
        super()._post_clean()
        password = self.cleaned_data.get('password')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error('password', error)


class StaffForm(ModelForm):
    address = forms.CharField(max_length=255, required=True)

    class Meta:
        model = Staff
        fields = ('address',)


class UserStudentForm(ModelForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['autofocus'] = True

    def save(self, commit=True, **kwargs):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.user_type = 3
        if commit:
            user.save()
            user.student.student_id = kwargs['form'].cleaned_data['student_id']
            user.student.address = kwargs['form'].cleaned_data['address']
            user.student.gender = kwargs['form'].cleaned_data['gender']
            user.student.session = kwargs['form'].cleaned_data['session']
            user.student.course = kwargs['form'].cleaned_data['course']
            print(user.student.id)
            print(user.student.student_id)
            # user.student.profile_pic = kwargs['form'].cleaned_data['profile_pic']
            user.save()
        return user

    def _post_clean(self):
        super()._post_clean()
        password = self.cleaned_data.get('password')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error('password', error)


class StudentForm(ModelForm):
    address = forms.CharField(max_length=255, required=True)

    class Meta:
        model = Student
        exclude = ('user',)
