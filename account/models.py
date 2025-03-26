from django.db import models
from django.contrib.auth.models import AbstractUser
from role.models import Role
# Create your models here.
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Tạo user với email thay vì username"""
        if not email:
            raise ValueError("Email là bắt buộc")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Tạo superuser với quyền admin"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class Account(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.ForeignKey('role.Role', on_delete=models.CASCADE, related_name="role_accounts")
    employee = models.OneToOneField('employee.Employee', on_delete=models.CASCADE, null=True,  # Cho phép giá trị NULL
    blank=True, related_name='employee_account')
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    username = None  # Xóa username
    USERNAME_FIELD = 'email'  # Đăng nhập bằng email
    REQUIRED_FIELDS = []  # Không yêu cầu trường nào khác

    objects = AccountManager()  # Sử dụng custom manager

    def __str__(self):
        return self.email

    class Meta:
      db_table = 'accounts'
      verbose_name = "Tài khoản"
      verbose_name_plural = "Các tài khoản"