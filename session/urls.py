from django.urls import path
from session.views import SessionListView, SessionCreateView, SessionUpdateView


urlpatterns = [
    path('', SessionListView.as_view(), name='list'),
    path('new/', SessionCreateView.as_view(), name='new'),
    path('edit/<int:pk>', SessionUpdateView.as_view(), name='edit')
]
