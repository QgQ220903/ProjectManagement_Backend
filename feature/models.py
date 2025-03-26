from django.db import models

# Create your models here.
class Feature(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    class Meta:
      db_table = 'features'
      verbose_name = "Chức năng"
      verbose_name_plural = "Các chức năng"