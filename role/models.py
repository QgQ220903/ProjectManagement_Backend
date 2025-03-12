from django.db import models

# Create your models here.
class Role(models.Model):
    name = models.CharField(max_length=255, verbose_name="Tên nhóm quyền")
    status = models.BooleanField(default=False, verbose_name="Trạng thái")
    

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'roles' 
        verbose_name = "Nhóm quyền"
        verbose_name_plural = "Các nhóm quyền"
