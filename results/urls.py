from django.urls import path
from results.views import ResultCreateView, ResultUpdateView, ResultListView

urlpatterns = [
    path('new/', ResultCreateView.as_view(), name='new'),
    path('edit/', ResultUpdateView.as_view(), name='edit'),
    path('', ResultListView.as_view(), name='list')
]
