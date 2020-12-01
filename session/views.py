from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from session.models import Session
from session.forms import SessionForm


class SessionListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'admin/session/session_list.html'
    model = Session

    def test_func(self):
        return True if self.request.user.user_type == '1' else False


class SessionCreateView(SuccessMessageMixin, UserPassesTestMixin, LoginRequiredMixin, CreateView):
    template_name = 'admin/session/session_form.html'
    model = Session
    form_class = SessionForm
    success_message = "Session created successfully"

    def test_func(self):
        return True if self.request.user.user_type == '1' else False

    def get_success_url(self):
        return reverse('session:list')


class SessionUpdateView(SuccessMessageMixin, UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    template_name = 'admin/session/session_form.html'
    model = Session
    form_class = SessionForm
    success_message = "Session updated successfully"

    def test_func(self):
        return True if self.request.user.user_type == '1' else False

    def get_success_url(self):
        return reverse('session:list')
