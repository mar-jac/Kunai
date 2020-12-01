from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.views.generic import View, ListView, CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
import json
import requests
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from users.models import CustomUser, Staff, Student
from subjects.models import Subject
from users.forms import UserStaffForm, StaffForm, UserStudentForm, StudentForm
from users.serializers import StudentSerializer
from attendance.models import Attendance, AttendanceReport
from leaves.models import LeaveReportStaff, LeaveReportStudent
from courses.models import Course
from subjects.models import Subject
from feedback.models import FeedbackStaff, FeedbackStudent
from notifications.models import NotificationStaff, NotificationStudent


def get_student_stats(student):
    subject_list = []
    present_list = []
    absent_list = []
    for subject in student.course.subject_set.all():
        attendance = Attendance.objects.filter(subject=subject)
        present_count = AttendanceReport.objects.filter(attendance__in=attendance, status=True,
                                                        student=student).count()
        absent_count = AttendanceReport.objects.filter(attendance__in=attendance, status=False,
                                                       student=student).count()
        subject_list.append(subject.subject_name)
        present_list.append(present_count)
        absent_list.append(absent_count)
    return {
        'pending_notifications': NotificationStudent.objects.filter(read=False).count(),
        'presents': AttendanceReport.objects.filter(student=student, status=True).count(),
        'absents': AttendanceReport.objects.filter(student=student, status=False).count(),
        'total_subjects': student.course.subject_set.count(),
        'subject_list': subject_list,
        'present_list': present_list,
        'absent_list': absent_list
    }


def get_staff_stats(staff):
    subjects = Subject.objects.filter(staff=staff)
    course_id_list = []
    for subject in subjects:
        course_id = subject.course.id
        if not course_id in course_id_list:
            course_id_list.append(course_id)
    subject_list = []
    attendance_list = []
    for subject in subjects:
        subject_list.append(subject.subject_name)
        attendance_list.append(Attendance.objects.filter(subject=subject).count())
    students = Student.objects.filter(course__in=course_id_list)
    student_list = []
    absent_list = []
    present_list = []
    for student in students:
        present_count = AttendanceReport.objects.filter(status=True, student_id=student.id).count()
        absent_count = AttendanceReport.objects.filter(status=False, student_id=student.id).count()
        student_list.append(student.user.username)
        present_list.append(present_count)
        absent_list.append(absent_count)
    return {
        'pending_notifications': NotificationStaff.objects.filter(read=False).count(),
        'total_attendance': Attendance.objects.filter(subject__in=subjects).count(),
        'total_leaves': LeaveReportStaff.objects.filter(staff=staff, leave_status=2).count(),
        'total_subjects': subjects.count(),
        'subject_list': subject_list,
        'attendance_list': attendance_list,
        'student_list': student_list,
        'present_list': present_list,
        'absent_list': absent_list
    }


def get_admin_stats(admin):
    staff_list = []
    staff_present_list = []
    staff_absent_list = []
    for staff in Staff.objects.all():
        subjects = Subject.objects.filter(staff=staff)
        attendance = Attendance.objects.filter(subject__in=subjects).count()
        leaves = LeaveReportStaff.objects.filter(staff=staff, leave_status=2).count()
        staff_present_list.append(attendance)
        staff_absent_list.append(leaves)
        staff_list.append(staff.user.username)
    student_list = []
    student_present_list = []
    student_absent_list = []
    for student in Student.objects.all():
        attendance = AttendanceReport.objects.filter(student=student, status=True).count()
        absent = AttendanceReport.objects.filter(student=student, status=False).count()
        leaves = LeaveReportStudent.objects.filter(student=student.id, leave_status=2).count()
        student_present_list.append(attendance)
        student_absent_list.append(leaves+absent)
        student_list.append(student.user.username)
    return {
        'pending_staff_leaves': LeaveReportStaff.objects.filter(leave_status='1').count(),
        'pending_student_leaves': LeaveReportStudent.objects.filter(leave_status='1').count(),
        'staff_feedbacks': FeedbackStaff.objects.count(),
        'student_feedbacks': FeedbackStudent.objects.count(),
        'total_students': Student.objects.count(),
        'total_staff': Staff.objects.count(),
        'total_courses': Course.objects.count(),
        'total_subjects': Subject.objects.count(),
        'staff_list': staff_list,
        'staff_present_list': staff_present_list,
        'staff_absent_list': staff_absent_list,
        'student_list': student_list,
        'student_present_list': student_present_list,
        'student_absent_list': student_absent_list
    }


class UserLoginView(LoginView):
    template_name = 'login.html'

    def post(self, request, *args, **kwargs):
        captcha_token = request.POST.get("g-recaptcha-response")
        cap_url = "https://www.google.com/recaptcha/api/siteverify"
        cap_secret = '6LfNSvQZAAAAAJ93dzhRG6i8R7AAg1eRZ4hE7Q5g'
        cap_data = {"secret": cap_secret, "response": captcha_token}
        cap_server_response = requests.post(url=cap_url, data=cap_data)
        cap_json = json.loads(cap_server_response.text)
        if cap_json['success'] == False:
            messages.error(request, "Invalid Captcha! Try Again")
            return redirect('login')
        return super().post(request, *args, **kwargs)


class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.user_type == '1':
            return render(request, 'admin/home.html', context=get_admin_stats(request.user.admin))
        if request.user.user_type == '2':
            return render(request, 'staff/home.html', context=get_staff_stats(request.user.staff))
        if request.user.user_type == '3':
            return render(request, 'student/home.html', context=get_student_stats(request.user.student))


class StaffListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'admin/users/staff_list.html'
    model = Staff

    def test_func(self):
        return True if self.request.user.user_type == '1' else False


class StaffCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = 'admin/users/staff_form.html'
    model = CustomUser
    form_class = UserStaffForm

    def test_func(self):
        return True if self.request.user.user_type == '1' else False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'form2' not in context:
            context['form2'] = StaffForm()
        return context

    def post(self, request, *args, **kwargs):
        user_staff_form = UserStaffForm(request.POST)
        staff_form = StaffForm(request.POST)
        if user_staff_form.is_valid() and staff_form.is_valid():
            user_staff_form.save(form=staff_form)
            messages.success(request, 'Staff added successfully')
            return redirect('users:list_staff')
        context = {'form': user_staff_form, 'form2': staff_form}
        return render(request, self.template_name, context=context)


class StaffUpdateView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'admin/users/staff_form.html'
    model = CustomUser
    form_class = UserStaffForm
    success_message = "Staff memeber added successfully"

    def test_func(self):
        if CustomUser.objects.get(id=self.kwargs['pk']).user_type == '2' and self.request.user.user_type == '1':
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'form2' not in context:
            context['form2'] = StaffForm(instance=CustomUser.objects.get(id=self.kwargs['pk']).staff)
        return context

    def post(self, request, pk, **kwargs):
        user = CustomUser.objects.get(id=pk)
        user_staff_form = UserStaffForm(request.POST, instance=user)
        staff_form = StaffForm(request.POST, instance=user.staff)
        if user_staff_form.is_valid() and staff_form.is_valid():
            user_staff_form.save(form=staff_form)
            messages.success(request, 'Staff added successfully')
            return redirect('users:list_staff')
        context = {'form': user_staff_form, 'form2': staff_form}
        return render(request, self.template_name, context=context)


class StudentListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'admin/users/student_list.html'
    model = Student

    def test_func(self):
        if 'subject' in self.request.GET and self.request.user.user_type == '2':
            return True
        return True if self.request.user.user_type == '1' else False

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            students = Student.objects.filter(course=Subject.objects.get(id=request.GET['subject']).course,
                                              session_id=request.GET['session'])
            serialized_students = StudentSerializer(students, many=True).data
            return JsonResponse(serialized_students, safe=False)
        return super().get(request, *args, **kwargs)


class StudentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = 'admin/users/student_form.html'
    model = CustomUser
    form_class = UserStudentForm

    def test_func(self):
        return True if self.request.user.user_type == '1' else False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'form2' not in context:
            context['form2'] = StudentForm()
        return context

    def post(self, request, *args, **kwargs):
        user_student_form = UserStudentForm(request.POST)
        student_form = StudentForm(request.POST, request.FILES)
        if user_student_form.is_valid() and student_form.is_valid():
            user_student_form.save(form=student_form)
            messages.success(request, 'Student added successfully')
            return redirect('users:list_student')
        context = {'form': user_student_form, 'form2': student_form}
        return render(request, self.template_name, context=context)


class StudentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'admin/users/student_form.html'
    model = CustomUser
    form_class = UserStudentForm

    def test_func(self):
        if CustomUser.objects.get(id=self.kwargs['pk']).user_type == '3' and self.request.user.user_type == '1':
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'form2' not in context:
            context['form2'] = StudentForm(instance=CustomUser.objects.get(id=self.kwargs['pk']).student)
        return context

    def post(self, request, pk, **kwargs):
        user = CustomUser.objects.get(id=pk)
        user_student_form = UserStudentForm(request.POST, instance=user)
        student_form = StudentForm(request.POST, request.FILES, instance=user.student)
        if user_student_form.is_valid() and student_form.is_valid():
            user_student_form.save(form=student_form)
            messages.success(request, 'Student updated successfully')
            return redirect('users:list_student')
        context = {'form': user_student_form, 'form2': student_form}
        return render(request, self.template_name, context=context)
