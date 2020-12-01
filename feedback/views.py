from django.shortcuts import render, reverse
from django.views.generic import View, ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from feedback.forms import StaffFeedbackForm, StudentFeedbackForm, StaffReplyForm, StudentReplyForm
from feedback.models import FeedbackStaff, FeedbackStudent


class StaffFeedbackCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = 'staff/feedback/feedback_form.html'
    model = FeedbackStaff
    form_class = StaffFeedbackForm

    def test_func(self):
        return True if self.request.user.user_type == '2' else False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = FeedbackStaff.objects.all().order_by('-id')
        return context

    def form_valid(self, form):
        form.instance.staff = self.request.user.staff
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('feedback:new_staff')


class StudentFeedbackCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = 'student/feedback/feedback_form.html'
    model = FeedbackStudent
    form_class = StudentFeedbackForm

    def test_func(self):
        return True if self.request.user.user_type == '3' else False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = FeedbackStudent.objects.all().order_by('-id')
        return context

    def form_valid(self, form):
        form.instance.student = self.request.user.student
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('feedback:new_student')


class StaffFeedbackListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = FeedbackStaff
    template_name = 'admin/feedback/staff_feedback_list.html'

    def test_func(self):
        return True if self.request.user.user_type == '1' else False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = StaffReplyForm()
        return context


class StaffFeedbackUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = FeedbackStaff
    form_class = StaffReplyForm

    def test_func(self):
        return True if self.request.user.user_type == '1' else False

    def get_success_url(self):
        return reverse('feedback:list_staff')


class StudentFeedbackListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = FeedbackStudent
    template_name = 'admin/feedback/student_feedback_list.html'

    def test_func(self):
        return True if self.request.user.user_type == '1' else False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = StaffReplyForm()
        return context


class StudentFeedbackUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = FeedbackStudent
    form_class = StudentReplyForm

    def test_func(self):
        return True if self.request.user.user_type == '1' else False

    def get_success_url(self):
        return reverse('feedback:list_student')
