from django.db import models
from django.contrib.auth.models import AbstractUser
from role.models import Role
# Create your models here.
class User(AbstractUser):  # Kế thừa từ AbstractUser để dùng hệ thống auth của Django
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, related_name="users")

    class Meta:
        db_table = 'users'