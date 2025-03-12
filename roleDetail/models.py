from django.db import models
from role.models import Role
from feature.models import Feature
# Create your models here.
class RoleDetail(models.Model):
    roleId = models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name="Nhóm quyền")
    featureId = models.ForeignKey(Feature, on_delete=models.CASCADE, verbose_name="Chức năng")
    action = models.CharField(max_length=255, verbose_name="Hành động")
    
    def __str__(self):
        return f"{self.role.name} - {self.feature.name}"
    
    class Meta:
        db_table = 'role_detail'
        verbose_name = "Chi tiết quyền"
        verbose_name_plural = "Các chi tiết quyền"


