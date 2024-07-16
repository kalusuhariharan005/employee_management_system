# myapp/models.py
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone


class CustomUser(AbstractUser):
    role = models.CharField(max_length=255)
    groups = models.ManyToManyField(Group, related_name='customuser_set')
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set')

    def __str__(self):
        return self.username

class Attendance(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    clock_in = models.DateTimeField()
    clock_out = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.user} - {self.clock_in} to {self.clock_out}'

class LeaveRequest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} - {self.start_date} to {self.end_date}'
