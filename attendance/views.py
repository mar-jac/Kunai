from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse, Http404
from django.views.generic import View, ListView, CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from attendance.serializers import AttendanceSerializer, AttendanceReportSerializer
from attendance.models import Attendance, AttendanceReport
from users.models import Staff, Student
from subjects.models import Subject
from attendance.forms import AttendanceForm, AttendanceUpdateForm, AttendanceSearchForm


class AttendanceCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = 'staff/attendance/attendance_form.html'
    model = Attendance
    form_class = AttendanceForm

    def test_func(self):
        return True if self.request.user.user_type == '2' else False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AttendanceForm(staff=Staff.objects.get(user=self.request.user))
        return context

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        for student in Student.objects.filter(course=Subject.objects.get(id=request.POST['subject']).course):
            if str(student.id) in request.POST.getlist('student[]'):
                AttendanceReport.objects.create(attendance=self.object, student=student, status=True)
            else:
                AttendanceReport.objects.create(attendance=self.object, student=student, status=False)
        return redirect('home')

    def get_success_url(self, **kwargs):
        return reverse('home')


class AttendanceDetailView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'staff/attendance/attendance_detail.html'

    def test_func(self):
        return True if self.request.user.user_type == '2' else False

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            attendance_reports = AttendanceReport.objects.filter(attendance_id=request.GET['attendance'])
            serialized_reports = AttendanceReportSerializer(attendance_reports, many=True).data
            return JsonResponse(serialized_reports, safe=False)
        context = {'form': AttendanceUpdateForm(staff=Staff.objects.get(user=self.request.user))}
        return render(request, self.template_name, context=context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AttendanceUpdateForm(staff=Staff.objects.get(user=self.request.user))
        return context


class AttendanceUpdateView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return True if self.request.user.user_type == '2' else False

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            attendances = Attendance.objects.filter(subject_id=request.GET['subject'],
                                                    session_id=request.GET['session'])
            serialized_attendance = AttendanceSerializer(attendances, many=True).data
            return JsonResponse(serialized_attendance, safe=False)
        raise Http404

    def post(self, request, *args, **kwargs):
        attendance = Attendance.objects.get(id=request.POST['attendance_date'])
        for attendance_report in attendance.attendancereport_set.all():
            attendance_report.status = str(attendance_report.id) in request.POST.getlist('report[]')
            attendance_report.save()
        return redirect('home')


class AttendanceStudentView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'student/attendance/attendance_search.html'

    def test_func(self):
        return True if self.request.user.user_type == '3' else False

    def get(self, request, *args, **kwargs):
        if 'start_date' in request.GET and 'end_date' in request.GET:
            attendances = Attendance.objects.filter(subject=request.GET['subject'], attendance_date__range=[
                                                    request.GET['start_date'], request.GET['end_date']])
            reports = []
            for attendance in attendances:
                report_qs = AttendanceReport.objects.filter(attendance=attendance, student=request.user.student)
                if report_qs.exists():
                    reports.append(report_qs[0])
            context = {'object_list': reports}
            return render(request, 'student/attendance/attendance_list.html', context=context)
        context = {'form': AttendanceSearchForm(course=request.user.student.course)}
        return render(request, self.template_name, context=context)
