from django.db import models


# Create your models here.
class Account(models.Model):
    employee_id = models.IntegerField(primary_key=True, verbose_name="Mã nhân viên")  # Mã nhân viên là khóa chính
    role_id = models.IntegerField(verbose_name="Mã nhóm quyền")  # Mã nhóm quyền là khóa ngoại
    username = models.CharField(max_length=255, unique=True, verbose_name="Tên tài khoản")  # nvarchar(MAX)
    password = models.CharField(max_length=255, verbose_name="Mật khẩu")  # nvarchar(MAX)
    status = models.BooleanField(default=True, verbose_name="Trạng thái")  # bit


    def __str__(self):
        return self.username


    class Meta:
        db_table = 'accounts'  # Tên bảng trong database
        verbose_name = "Tài khoản"
        verbose_name_plural = "Các tài khoản"
        ordering = ['username']  # Sắp xếp theo tên tài khoản tăng dần
