from django.urls import path
from subjects.views import SubjectListView, SubjectCreateView, SubjectUpdateView


urlpatterns = [
    path('', SubjectListView.as_view(), name='list'),
    path('new/', SubjectCreateView.as_view(), name='new'),
    path('edit/<int:pk>', SubjectUpdateView.as_view(), name='edit')
]
