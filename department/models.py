from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    manager = models.OneToOneField('employee.Employee', on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_department')
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
      db_table = 'departments'
      verbose_name = "Phòng Ban"
      verbose_name_plural = "Các phòng ban"