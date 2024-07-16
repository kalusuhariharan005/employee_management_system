from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, LeaveRequestForm
from .models import Attendance, LeaveRequest

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return render(request, 'registration/logout.html')

@login_required
def clock_in_view(request):
    if request.method == 'POST':
        Attendance.objects.create(user=request.user, clock_in=timezone.now())
        return redirect('attendance_history')
    return render(request, 'attendance/clock_in.html')

@login_required
def clock_out_view(request):
    if request.method == 'POST':
        attendance = Attendance.objects.filter(user=request.user, clock_out__isnull=True).last()
        if attendance:
            attendance.clock_out = timezone.now()
            attendance.save()
        return redirect('attendance_history')
    return render(request, 'attendance/clock_out.html')

@login_required
def attendance_history_view(request):
    attendances = Attendance.objects.filter(user=request.user)
    return render(request, 'attendance/attendance_history.html', {'attendances': attendances})

@login_required
def leave_request_view(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave_request = form.save(commit=False)
            leave_request.user = request.user
            leave_request.save()
            return redirect('leave_history')
    else:
        form = LeaveRequestForm()
    return render(request, 'leave/leave_request.html', {'form': form})

@login_required
def leave_history_view(request):
    leave_requests = LeaveRequest.objects.filter(user=request.user)
    return render(request, 'leave/leave_history.html', {'leave_requests': leave_requests})

@login_required
def approve_leave_view(request, leave_id):
    leave_request = get_object_or_404(LeaveRequest, id=leave_id)
    leave_request.approved = True
    leave_request.save()
    return redirect('leave_requests')
