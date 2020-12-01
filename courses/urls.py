from django.urls import path
from courses.views import CourseListView, CourseCreateView, CourseUpdateView


urlpatterns = [
    path('', CourseListView.as_view(), name='list'),
    path('new/', CourseCreateView.as_view(), name='new'),
    path('edit/<int:pk>', CourseUpdateView.as_view(), name='edit')
]
