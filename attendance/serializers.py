from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from attendance.models import Attendance, AttendanceReport
from users.serializers import StudentSerializer


class AttendanceSerializer(ModelSerializer):
    class Meta:
        model = Attendance
        fields = ('id', 'attendance_date')


class AttendanceReportSerializer(ModelSerializer):
    student = StudentSerializer()

    class Meta:
        model = AttendanceReport
        fields = '__all__'
