from django.shortcuts import render, reverse, redirect
from django.http import JsonResponse, Http404
from django.views.generic import View, CreateView, ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from users.models import Staff, Student
from results.models import Result
from results.forms import ResultForm
from results.serializers import ResultSerializer


class ResultCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = 'staff/results/result_form.html'
    model = Result
    form_class = ResultForm

    def test_func(self):
        return True if self.request.user.user_type == '2' else False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ResultForm(staff=Staff.objects.get(user=self.request.user))
        return context

    def get_success_url(self, **kwargs):
        return reverse('home')


class ResultUpdateView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'staff/results/result_edit.html'

    def test_func(self):
        return True if self.request.user.user_type == '2' else False

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            result_qs = Result.objects.filter(student_id=request.GET['student'], subject_id=request.GET['subject'])
            serialized_results = ResultSerializer(result_qs, many=True).data
            return JsonResponse(serialized_results, safe=False)
        context = {'form': ResultForm(staff=Staff.objects.get(user=self.request.user))}
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        result_qs = Result.objects.filter(student_id=request.POST['student'], subject_id=request.POST['subject'])
        if result_qs.exists():
            result = result_qs[0]
            result.assignment_marks = float(request.POST['assignment_marks'])
            result.exam_marks = float(request.POST['exam_marks'])
            result.save()
        return redirect('home')


class ResultListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'student/results/result_list.html'
    model = Result

    def test_func(self):
        return True if self.request.user.user_type == '3' else False

    def get_queryset(self):
        return Result.objects.filter(student=self.request.user.student)
