from django.db import models

class Feature(models.Model):
    name = models.CharField(max_length=255, verbose_name="Tên chức năng")
    status = models.BooleanField(default=False, verbose_name="Trạng thái")
    

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'features' 
        verbose_name = "Chức năng"
        verbose_name_plural = "Các chức năng"
