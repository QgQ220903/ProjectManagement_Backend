from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=255, verbose_name="Tên dự án")
    isDeleted = models.BooleanField(default=False, verbose_name="Đã xóa")
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'projects'
        verbose_name = "Dự án"
        verbose_name_plural = "Các dự án"

class ProjectPart(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="Dự án")
    name = models.CharField(max_length=255, verbose_name="Tên phần dự án")
    isDeleted = models.BooleanField(default=False, verbose_name="Đã xóa")
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'project_parts'
        verbose_name = "Phần dự án"
        verbose_name_plural = "Các phần dự án"