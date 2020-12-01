from django.shortcuts import render, redirect, reverse
from django.views.generic import View, ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from notifications.models import NotificationStaff, NotificationStudent
from notifications.forms import NotificationStaffForm, NotificationStudentForm


class StaffNotificationCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    template_name = 'admin/notifications/notification_form.html'
    model = NotificationStaff
    form_class = NotificationStaffForm
    success_message = "Notification sent successfully"

    def test_func(self):
        return True if self.request.user.user_type == '1' else False

    def get_success_url(self):
        return reverse('home')


class StudentNotificationCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    template_name = 'admin/notifications/notification_form.html'
    model = NotificationStudent
    form_class = NotificationStudentForm
    success_message = "Notification sent successfully"

    def test_func(self):
        return True if self.request.user.user_type == '1' else False

    def get_success_url(self):
        return reverse('home')


class StaffNotificationListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'staff/notifications/notification_list.html'
    model = NotificationStaff

    def test_func(self):
        return True if self.request.user.user_type == '2' else False


class StudentNotificationListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'student/notifications/notification_list.html'
    model = NotificationStudent

    def test_func(self):
        return True if self.request.user.user_type == '3' else False


class StaffNotificationUpdateView(LoginRequiredMixin, UserPassesTestMixin, View):
    http_method_names = ['get']

    def test_func(self):
        return True if self.request.user.user_type == '2' else False

    def get(self, request, pk, **kwargs):
        notification = NotificationStaff.objects.get(id=pk)
        notification.read = True
        notification.save()
        return redirect('notifications:list_staff')


class StudentNotificationUpdateView(LoginRequiredMixin, UserPassesTestMixin, View):
    http_method_names = ['get']

    def test_func(self):
        return True if self.request.user.user_type == '3' else False

    def get(self, request, pk, **kwargs):
        notification = NotificationStudent.objects.get(id=pk)
        notification.read = True
        notification.save()
        return redirect('notifications:list_student')
