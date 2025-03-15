from django.db import models
from department.models import Department  # Import model Department

class Employee(models.Model):
    department = models.ForeignKey(
        Department, 
        on_delete=models.CASCADE, 
        verbose_name="Mã phòng ban"
    )
    positionName = models.CharField(max_length=255, verbose_name="Tên chức vụ")
    employeeName = models.CharField(max_length=255, verbose_name="Tên nhân viên")
    employeePhone = models.CharField(max_length=255, verbose_name="Số điện thoại")
    employeeEmail = models.CharField(max_length=255, verbose_name="Email")
    status = models.BooleanField(default=True, verbose_name="Trạng thái")

    def __str__(self):
        return self.employeeName
