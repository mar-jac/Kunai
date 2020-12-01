from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from courses.models import Course
from courses.forms import CourseForm


class CourseListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'admin/courses/course_list.html'
    model = Course

    def test_func(self):
        return True if self.request.user.user_type == '1' else False


class CourseCreateView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = 'admin/courses/course_form.html'
    model = Course
    form_class = CourseForm
    success_message = "Course created successfully"

    def test_func(self):
        return True if self.request.user.user_type == '1' else False

    def get_success_url(self):
        return reverse('courses:list')


class CourseUpdateView(SuccessMessageMixin, UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    template_name = 'admin/courses/course_form.html'
    model = Course
    form_class = CourseForm
    success_message = "Course updated successfully"

    def test_func(self):
        return True if self.request.user.user_type == '1' else False

    def get_success_url(self):
        return reverse('courses:list')
