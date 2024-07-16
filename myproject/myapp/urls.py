from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('clock-in/', views.clock_in_view, name='clock_in'),
    path('clock-out/', views.clock_out_view, name='clock_out'),
    path('attendance-history/', views.attendance_history_view, name='attendance_history'),
    path('leave-request/', views.leave_request_view, name='leave_request'),
    path('leave-history/', views.leave_history_view, name='leave_history'),
    path('approve-leave/<int:leave_id>/', views.approve_leave_view, name='approve_leave'),
]
