from django.db import models

class Employee(models.Model):
    POSITION_CHOICES = (
        ('TP', 'Trưởng phòng'),
        ('NV', 'Nhân viên'),
    )
    department = models.ForeignKey('department.Department', on_delete=models.CASCADE, related_name='employees')
    position = models.CharField(max_length=2, choices=POSITION_CHOICES)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
      db_table = 'employees'
      verbose_name = "Nhân Viên"
      verbose_name_plural = "Các nhân viên"