# project_part/models.py
from django.db import models
from department.models import Department

class ProjectPart(models.Model):
    project = models.ForeignKey('project.Project', on_delete=models.CASCADE, related_name='project_parts')
    name = models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name="project_parts")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'project_parts'
        verbose_name = "Phần dự án"
        verbose_name_plural = "Các phần dự án"
