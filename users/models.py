from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from courses.models import Course
from session.models import Session


class CustomUser(AbstractUser):
    USER_TYPES = (
        (1, 'HOD'),
        (2, 'Staff'),
        (3, 'Student')
    )

    user_type = models.CharField(max_length=1, choices=USER_TYPES, default=1)


class Admin(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Staff(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Student(models.Model):
    GENDER_TYPES = (
        (1, 'Male'),
        (2, 'Female'),
        (3, 'Non_Binary'),
        (4, 'Other')
    )

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    student_id = models.IntegerField(unique=True, validators=[MinValueValidator(10000000), MaxValueValidator(99999999)])
    gender = models.IntegerField(choices=GENDER_TYPES)
    # profile_pic = models.ImageField(upload_to='students/')
    address = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            Admin.objects.create(user=instance)
        if instance.user_type == 2:
            Staff.objects.create(user=instance, address='')
        if instance.user_type == 3:
            Student.objects.create(
                student_id=1, user=instance, course=Course.objects.first(),
                session=Session.objects.first(), address="", gender=1)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.admin.save()
    if instance.user_type == 2:
        instance.staff.save()
    if instance.user_type == 3:
        instance.student.save()
