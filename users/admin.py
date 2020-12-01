from django.contrib import admin
from users.models import CustomUser, Admin, Staff, Student


admin.site.register(CustomUser)
admin.site.register(Admin)
admin.site.register(Staff)
admin.site.register(Student)
