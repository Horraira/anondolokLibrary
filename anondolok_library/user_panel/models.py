from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Appointments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    user_name = models.CharField(max_length=200, null=True)
    appointment_date = models.DateField(auto_now_add=True, null=True, blank=True)
    requested_date = models.DateField(blank=True, null=True)
    requested_time = models.TimeField(blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    check_approve = models.IntegerField(default=2)

    def __str__(self):
        return str(self.user_name)

