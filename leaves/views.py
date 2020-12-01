from django.shortcuts import render, redirect, reverse
from django.views.generic import View, ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from leaves.forms import StaffLeaveForm, StudentLeaveForm
from leaves.models import LeaveReportStaff, LeaveReportStudent


class StaffLeaveCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = 'staff/leaves/leave_form.html'
    model = LeaveReportStaff
    form_class = StaffLeaveForm

    def test_func(self):
        return True if self.request.user.user_type == '2' else False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = LeaveReportStaff.objects.all().order_by('-id')
        return context

    def form_valid(self, form):
        form.instance.staff = self.request.user.staff
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('leaves:new_staff')


class StudentLeaveCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = 'student/leaves/leave_form.html'
    model = LeaveReportStudent
    form_class = StudentLeaveForm

    def test_func(self):
        return True if self.request.user.user_type == '3' else False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = LeaveReportStudent.objects.all().order_by('-id')
        return context

    def form_valid(self, form):
        form.instance.student = self.request.user.student
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('leaves:new_student')


class StaffLeaveListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'admin/leaves/staff_leave_list.html'
    model = LeaveReportStaff

    def test_func(self):
        return True if self.request.user.user_type == '1' else False


class StaffLeaveUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = LeaveReportStaff

    def test_func(self):
        return True if self.request.user.user_type == '1' else False

    def post(self, request, pk, **kwargs):
        report = LeaveReportStaff.objects.get(id=pk)
        report.leave_status = request.POST['status']
        report.save()
        return redirect('leaves:list_staff')


class StudentLeaveListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'admin/leaves/student_leave_list.html'
    model = LeaveReportStudent

    def test_func(self):
        return True if self.request.user.user_type == '1' else False


class StudentLeaveUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = LeaveReportStudent

    def test_func(self):
        return True if self.request.user.user_type == '1' else False

    def post(self, request, pk, **kwargs):
        report = LeaveReportStudent.objects.get(id=pk)
        report.leave_status = request.POST['status']
        report.save()
        return redirect('leaves:list_student')
