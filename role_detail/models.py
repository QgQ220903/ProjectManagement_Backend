from django.db import models
from role.models import Role
from feature.models import Feature
# Create your models here.
class RoleDetail(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="role_details")
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, related_name="feature_details")
    can_view = models.BooleanField(default=False)
    can_create = models.BooleanField(default=False)
    can_update = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.role.name} - {self.feature.name}"
    class Meta:
        db_table = 'role_details'
        verbose_name = "Chi tiết quyền"
        verbose_name_plural = "Các chi tiết quyền"