"""kunai URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import (
    LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
)
from users.views import HomeView, UserLoginView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('attendance/', include(('attendance.urls', 'attendance'), namespace='attendance')),
    path('courses/', include(('courses.urls', 'courses'), namespace='courses')),
    path('feedback/', include(('feedback.urls', 'feedback'), namespace='feedback')),
    path('leaves/', include(('leaves.urls', 'leaves'), namespace='leaves')),
    path('notifications/', include(('notifications.urls', 'notifications'), namespace='notifications')),
    path('results/', include(('results.urls', 'results'), namespace='results')),
    path('session/', include(('session.urls', 'session'), namespace='session')),
    path('subjects/', include(('subjects.urls', 'subjects'), namespace='subjects')),
    path('users/', include(('users.urls', 'users'), namespace='users')),
    path('', HomeView.as_view(), name='home'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password_reset/', PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password_reset_done/', PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete', PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
