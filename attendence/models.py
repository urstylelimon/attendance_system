from django.db import models
from datetime import datetime, time

class Employee(models.Model):
    emp_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    total_hours = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, default="On Time")  # On Time, Late, Absent

    def calculate_hours_and_status(self):
        # Calculate working hours
        if self.check_in and self.check_out:
            check_in_time = datetime.combine(self.date, self.check_in)
            check_out_time = datetime.combine(self.date, self.check_out)
            hours = (check_out_time - check_in_time).total_seconds() / 3600
            self.total_hours = round(hours, 2)
        else:
            self.total_hours = 0.0

        # Check for lateness
        if self.check_in:
            late_threshold = time(10, 15)  # 10:15 AM
            if self.check_in > late_threshold:
                self.status = "Late"
            else:
                self.status = "On Time"
        else:
            self.status = "Absent"

    def save(self, *args, **kwargs):
        self.calculate_hours_and_status()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee.name} - {self.date}"
