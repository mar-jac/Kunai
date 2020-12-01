from django.db import models
from courses.models import Course
from users.models import Staff


class Subject(models.Model):
    subject_name = models.CharField(max_length=80)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject_name
