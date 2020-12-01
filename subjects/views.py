from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from subjects.models import Subject
from subjects.forms import SubjectForm


class SubjectListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'admin/subjects/subject_list.html'
    model = Subject

    def test_func(self):
        return True if self.request.user.user_type == '1' else False


class SubjectCreateView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = 'admin/subjects/subject_form.html'
    model = Subject
    form_class = SubjectForm
    success_message = "Subject created successfully"

    def test_func(self):
        return True if self.request.user.user_type == '1' else False

    def get_success_url(self):
        return reverse('subjects:list')


class SubjectUpdateView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'admin/subjects/subject_form.html'
    model = Subject
    form_class = SubjectForm
    success_message = "Subject updated successfully"

    def test_func(self):
        return True if self.request.user.user_type == '1' else False

    def get_success_url(self):
        return reverse('subjects:list')
