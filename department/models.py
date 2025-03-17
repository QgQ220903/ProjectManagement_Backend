from django.db import models

class Department(models.Model):
    managerID = models.IntegerField(verbose_name="Mã trưởng phòng")
    departmentName = models.CharField(max_length=255, verbose_name="Tên phòng ban")
    departmentStatus = models.BooleanField(default=True, verbose_name="Trạng thái")

    def __str__(self):
        return self.departmentName
    class Meta:
        db_table = "department"