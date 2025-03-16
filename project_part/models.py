from django.db import models
from project.models import Project
# Create your models here.
class ProjectPart(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="Dự án", related_name="project_parts")
    name = models.CharField(max_length=255, verbose_name="Tên phần dự án")
    is_deleted = models.BooleanField(default=False, verbose_name="Đã xóa")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'project_parts'
        verbose_name = "Phần dự án"
        verbose_name_plural = "Các phần dự án"